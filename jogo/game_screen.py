import pygame
from jogo.button import Button # Presumindo que este é o caminho correto para sua classe Button
import random
import sqlite3
import json
import os

GAME_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME_FOR_GAME = os.path.join(GAME_SCRIPT_DIR, "quiz_banco.db")

class GameScreen:
    """Tela principal do quiz com perguntas e interações."""

    def __init__(self, screen, assets, selected_level, selected_subjects_list):
        self.screen = screen
        self.assets = assets
        self.running_show_loop = True
        self.last_arrow_click_time = 0
        self.arrow_click_delay = 500

        self.answer_buttons = {
            "A": Button(40, 280, assets.answer_a_img),
            "B": Button(40, 380, assets.answer_b_img),
            "C": Button(40, 480, assets.answer_c_img),
            "D": Button(40, 580, assets.answer_d_img),
        }

        self.help_buttons = {
            "pular": Button(560, 620, assets.botao_pular3_img),
            "dica": Button(730, 620, assets.botao_dica3_img),
            "eliminar": Button(900, 620, assets.botao_eliminar3_img),
        }

        self.help_used_for_current_question = False
        self.current_question_data = None
        self.show_feedback_popup = False
        self.feedback_popup_message = ""
        self.popup_font = assets.small_font
        self.show_hint_box = False
        self.hint_font = assets.small_font
        self.eliminated_answers = []
        self.question_index = 0
        self.last_answer_was_correct = False
        self.help_lives_remaining = 3

        self.current_help_button_images = {
            "pular": assets.botao_pular3_img,
            "dica": assets.botao_dica3_img,
            "eliminar": assets.botao_eliminar3_img
        }

        self.popup_rect_for_positioning = None
        self.right_arrow_button = Button(0, 0, assets.right_arrow_img)
        self.left_arrow_button = Button(0, 0, assets.left_arrow_img)

        self.all_loaded_questions = self._load_questions_from_sqlite(DB_FILENAME_FOR_GAME, selected_level, selected_subjects_list)

        if not self.all_loaded_questions:
            print("ERRO CRÍTICO: Nenhuma pergunta disponível (nem do BD, nem placeholders). O jogo pode não funcionar.")
            self.all_loaded_questions = [{
                "text": "Erro: Perguntas não carregadas!",
                "answers": {"A": "-", "B": "-", "C": "-", "D": "-"},
                "correct_answer": "A",
                "tip": "Verifique o arquivo quiz_banco.db ou o código."
            }]

        self.question_text_font = self.assets.medium_font
        self.answer_text_font = getattr(self.assets, 'answer_font', self.assets.small_font)

        # NOVA VARIÁVEL PARA CONTROLAR O ESTADO DE VITÓRIA
        self.game_won = False


    def _get_placeholder_questions(self):
        print("Usando perguntas placeholder como fallback.")
        return [
            {"text": "Qual linguagem o Pygame usa?", "answers": {"A": "Python", "B": "Java", "C": "C#", "D": "Lua"}, "correct_answer": "A", "tip": "É uma linguagem de script muito popular."},
            {"text": "Qual o resultado de 2 elevado a 3?", "answers": {"A": "5", "B": "6", "C": "8", "D": "9"}, "correct_answer": "C", "tip": "Multiplique 2 por ele mesmo, 3 vezes."},
            {"text": "Qual a cor do cavalo branco de Napoleão?", "answers": {"A": "Preto", "B": "Marrom", "C": "Branco", "D": "Malhado"}, "correct_answer": "C", "tip": "A pergunta já contém a resposta!"}
        ]

    def _load_questions_from_sqlite(self, db_path, target_level, target_subjects_list):
        loaded_questions = []
        conn = None
        try:
            if not os.path.exists(db_path):
                print(f"ERRO: Arquivo de banco de dados SQLite '{db_path}' não encontrado!")
                return self._get_placeholder_questions()
            if not target_level or not target_subjects_list:
                print(f"ERRO: Nível ({target_level}) ou matérias ({target_subjects_list}) inválidos para consulta.")
                return self._get_placeholder_questions()

            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query_base = "SELECT id, text, answer_a, answer_b, answer_c, answer_d, correct_answer, tip, subject, level FROM questions"
            conditions = ["level = ?"]
            params = [target_level]
            if target_subjects_list:
                placeholders = ", ".join(["?"] * len(target_subjects_list))
                conditions.append(f"subject IN ({placeholders})")
                params.extend(target_subjects_list)
            query = f"{query_base} WHERE {' AND '.join(conditions)}"
            cursor.execute(query, tuple(params))
            db_rows = cursor.fetchall()
            for row in db_rows:
                loaded_questions.append({
                    "id": row["id"], "text": row["text"],
                    "answers": {"A": row["answer_a"], "B": row["answer_b"], "C": row["answer_c"], "D": row["answer_d"]},
                    "correct_answer": row["correct_answer"], "tip": row["tip"], "subject": row["subject"], "level": row["level"]
                })
            if loaded_questions:
                random.shuffle(loaded_questions)
                if len(loaded_questions) > 12:
                    loaded_questions = loaded_questions[:12]
                    print(f"Foram selecionadas 12 perguntas aleatórias para o jogo a partir das encontradas para os filtros.")
                else:
                    print(f"{len(loaded_questions)} perguntas encontradas e selecionadas para os filtros (limite de 12 não atingido ou igualado).")
            else:
                print(f"Nenhuma pergunta encontrada no SQLite para Nível: {target_level}, Matérias: {target_subjects_list}.")
        except sqlite3.Error as err:
            print(f"Erro ao carregar perguntas do SQLite: {err}.")
            loaded_questions = []
        finally:
            if conn: conn.close()
        if not loaded_questions:
            print("Nenhuma pergunta carregada do BD ou erro na consulta, usando placeholders.")
            return self._get_placeholder_questions()
        return loaded_questions

    def _setup_for_new_question(self):
        if not self.all_loaded_questions: # Se, mesmo após o fallback, não houver perguntas
            print("AVISO CRÍTICO: _setup_for_new_question chamado sem NENHUMA pergunta carregada.")
            self.current_question_data = {"text": "ERRO AO CARREGAR PERGUNTAS!", "answers": {"A": "Verifique console", "B": "-", "C": "-", "D": "-"}, "correct_answer": "A", "tip": "Problema com quiz_banco.db"}
            self.show_feedback_popup = False; self.show_hint_box = False; self.eliminated_answers = []
            self.last_answer_was_correct = False; self.help_used_for_current_question = False
            life_suffix = "0"
            for name_key in self.help_buttons:
                try:
                    image = getattr(self.assets, f"botao_{name_key}{life_suffix}_img")
                    if image: self.current_help_button_images[name_key] = image; self.help_buttons[name_key].image = image
                except AttributeError: pass
            return

        # Verifica se o índice da pergunta ultrapassou o número de perguntas disponíveis (APÓS UMA VITÓRIA)
        # Se game_won for true, _setup_for_new_question não deve tentar pegar uma nova pergunta.
        # A tela de vitória cuidará da saída.
        if self.game_won or self.question_index >= len(self.all_loaded_questions):
            # Isso pode acontecer se o jogo for vencido e por algum motivo esta função for chamada.
            # Ou se o question_index for incrementado além do limite.
            # Neste ponto, o jogo deveria ter terminado ou estar na tela de vitória.
            # Apenas evitamos um erro de índice aqui.
            print("Fim das perguntas ou jogo ganho, não configurando nova pergunta.")
            # Poderia definir running_show_loop para False aqui se a tela de vitória não o fizer.
            return


        if self.last_answer_was_correct and self.help_used_for_current_question:
            if self.help_lives_remaining > 0: self.help_lives_remaining -= 1

        # idx = self.question_index % len(self.all_loaded_questions) # O módulo não é mais ideal se queremos um fim após 12.
        # Usamos question_index diretamente, pois ele só será incrementado até len-1.
        idx = self.question_index
        self.current_question_data = self.all_loaded_questions[idx]

        self.show_feedback_popup = False; self.show_hint_box = False; self.eliminated_answers = []
        self.last_answer_was_correct = False; self.help_used_for_current_question = False
        life_suffix = str(self.help_lives_remaining)
        for name_key in self.help_buttons:
            try: image = getattr(self.assets, f"botao_{name_key}{life_suffix}_img")
            except AttributeError:
                image = getattr(self.assets, f"botao_{name_key}0_img", None)
                if self.help_lives_remaining > 0: print(f"AVISO: Imagem 'botao_{name_key}{life_suffix}_img' não encontrada. Usando fallback 'botao_{name_key}0_img'.")
            if image: self.current_help_button_images[name_key] = image; self.help_buttons[name_key].image = image
            else: print(f"AVISO CRÍTICO: Nenhuma imagem encontrada para {name_key} (nem com sufixo, nem fallback 0).")

    # NOVO MÉTODO PARA EXIBIR A TELA DE VITÓRIA
    def _display_win_screen(self):
        try:
            parabens_img_surface = self.assets.parabens_img
            parabens_rect = parabens_img_surface.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
            )
            self.screen.blit(self.assets.background, (0,0)) # Limpa com o fundo primeiro
            self.screen.blit(parabens_img_surface, parabens_rect)
        except AttributeError:
            print("ERRO: Imagem 'parabens_img' não encontrada nos assets. Exibindo texto de fallback.")
            fallback_font = pygame.font.Font(None, 80) # Fonte maior para o fallback
            text_surf = fallback_font.render("PARABÉNS, VOCÊ VENCEU!", True, (255, 215, 0)) # Dourado
            text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(self.assets.background, (0,0))
            self.screen.blit(text_surf, text_rect)

        pygame.display.update()

        # Espera por qualquer tecla ou clique para sair da tela de vitória
        waiting_for_input_to_exit_win_screen = True
        # Limpa eventos antigos para não sair imediatamente se um clique estiver "preso"
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        pygame.event.clear(pygame.KEYDOWN)

        while waiting_for_input_to_exit_win_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False # Permite fechar o jogo
                    waiting_for_input_to_exit_win_screen = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_input_to_exit_win_screen = False # Sai ao clicar ou teclar

            # Se o jogo for fechado aqui, self.running_show_loop já é False
            if not self.running_show_loop:
                break

            pygame.time.Clock().tick(30)

        self.running_show_loop = False # Garante que a tela GameScreen vai fechar após a tela de vitória


    def _wrap_text(self, text, font, max_width, text_color=(255,255,255)):
        # ... (código do _wrap_text mantido como na sua última versão)
        rendered_lines = []
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            words = paragraph.split(' ')
            current_line_str = ""
            for i, word in enumerate(words):
                line_candidate_str = current_line_str + (" " if current_line_str else "") + word
                candidate_width = font.render(line_candidate_str, True, text_color).get_width()
                word_width_alone = font.render(word, True, text_color).get_width()
                if candidate_width <= max_width:
                    current_line_str = line_candidate_str
                else:
                    if current_line_str:
                        rendered_lines.append(font.render(current_line_str, True, text_color))
                    current_line_str = word
                    if word_width_alone > max_width and current_line_str == word :
                         rendered_lines.append(font.render(current_line_str, True, text_color))
                         current_line_str = ""
            if current_line_str:
                rendered_lines.append(font.render(current_line_str, True, text_color))
        return rendered_lines

    def _display_feedback_popup(self):
        # ... (código mantido)
        if not self.show_feedback_popup: return
        w, h = 450, 150; x = (self.screen.get_width() - w) // 2; y = (self.screen.get_height() - h) // 2
        self.popup_rect_for_positioning = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255, 255, 255), self.popup_rect_for_positioning)
        pygame.draw.rect(self.screen, (0, 208, 171), self.popup_rect_for_positioning, 5)
        text_surface = self.popup_font.render(self.feedback_popup_message, True, (0, 208, 171))
        text_rect = text_surface.get_rect(center=self.popup_rect_for_positioning.center)
        self.screen.blit(text_surface, text_rect)

    def _display_hint_box(self):
        # ... (código mantido)
        if not self.show_hint_box or not self.current_question_data: return
        hint = self.current_question_data.get("tip", "Dica não disponível."); tip_image = getattr(self.assets, 'tip_box_img', None)
        w, h = tip_image.get_size() if tip_image else (250, 120); x, y = self.screen.get_width() - w - 50, 240
        if tip_image: self.screen.blit(tip_image, (x, y))
        else: pygame.draw.rect(self.screen, (200,200,200), (x,y,w,h)); pygame.draw.rect(self.screen, (0,0,0), (x,y,w,h), 2)
        padding, max_width_hint = 30, w - 60; words, lines, line = hint.split(' '), [], ""
        for word in words:
            test_line = line + word + " "
            if self.hint_font.render(test_line, True, (0,0,0)).get_width() <= max_width_hint: line = test_line
            else: lines.append(line.strip()); line = word + " "
        lines.append(line.strip())
        for i, txt in enumerate(lines):
            surf = self.hint_font.render(txt, True, (255,255,255)); self.screen.blit(surf, (x + padding, y + padding + i * self.hint_font.get_linesize()))

    def show(self):
        self._setup_for_new_question() # Configura a primeira pergunta

        # Limpeza inicial de eventos de clique (MANTIDO)
        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running_show_loop = False; return
            pygame.time.wait(10)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        self.running_show_loop = True
        while self.running_show_loop:
            # >>> INÍCIO: Verificação de Vitória <<<
            if self.game_won:
                self._display_win_screen()
                # self.running_show_loop foi setado para False dentro de _display_win_screen
                # para sair deste loop e do método show().
                continue # Ou break, para garantir saída imediata do while e ir para o return
            # >>> FIM: Verificação de Vitória <<<

            action_taken_this_frame = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False

                if self.show_feedback_popup and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action_taken_this_frame = True
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_arrow_click_time >= self.arrow_click_delay:
                        if self.last_answer_was_correct:
                            if self.right_arrow_button.rect.collidepoint(mouse_pos):
                                if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

                                # Se o jogo já foi ganho (após acertar a última pergunta),
                                # o clique na seta direita do popup de "VOCÊ VENCEU"
                                # deve apenas fechar o popup para que a tela de vitória seja mostrada.
                                # A transição para _display_win_screen ocorrerá no início do próximo frame do loop.
                                if self.game_won:
                                    self.show_feedback_popup = False
                                    # Não incrementa question_index nem chama _setup_for_new_question aqui
                                else:
                                    self.question_index += 1
                                    if self.question_index < len(self.all_loaded_questions):
                                        self._setup_for_new_question()
                                    else:
                                        # Isso não deveria acontecer se game_won foi setado corretamente
                                        print("Índice de pergunta fora dos limites após vitória aparente - checar lógica")
                                        self.game_won = True # Garante estado de vitória
                                    self.show_feedback_popup = False
                                self.last_arrow_click_time = current_time
                        else:
                            if self.left_arrow_button.rect.collidepoint(mouse_pos): # Errou, volta ao menu
                                if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                                self.running_show_loop = False
                                self.show_feedback_popup = False
                                self.last_arrow_click_time = current_time

            if not self.running_show_loop: break

            # Desenho da tela principal do jogo (perguntas, botões, etc.)
            self.screen.blit(self.assets.background, (0, 0))
            box_x = (self.screen.get_width() - 968) // 2
            self.screen.blit(self.assets.question_box_img, (box_x, 20))

            # Renderização da pergunta com quebra de linha
            question_text_str = self.current_question_data.get("text", "...") if self.current_question_data else "..."
            padding_interno_caixa_x_perg = 45
            largura_maxima_para_texto_perg = 968 - (2 * padding_interno_caixa_x_perg)
            superficies_das_linhas_perg = self._wrap_text(question_text_str, self.question_text_font, largura_maxima_para_texto_perg)
            y_inicial_caixa_img_perg = 20
            padding_do_topo_da_caixa_perg = 25
            y_para_desenhar_linha_atual_perg = y_inicial_caixa_img_perg + padding_do_topo_da_caixa_perg
            espacamento_entre_linhas_renderizadas_perg = 4
            for superficie_linha_perg in superficies_das_linhas_perg:
                x_linha_perg = box_x + padding_interno_caixa_x_perg + (largura_maxima_para_texto_perg - superficie_linha_perg.get_width()) // 2
                self.screen.blit(superficie_linha_perg, (x_linha_perg, y_para_desenhar_linha_atual_perg))
                y_para_desenhar_linha_atual_perg += superficie_linha_perg.get_height() + espacamento_entre_linhas_renderizadas_perg

            if self.show_feedback_popup:
                self._display_feedback_popup()
                if self.popup_rect_for_positioning:
                    arrow_y = self.popup_rect_for_positioning.bottom + 20
                    btn_to_draw = self.right_arrow_button if self.last_answer_was_correct else self.left_arrow_button
                    btn_to_draw.rect.centerx = self.popup_rect_for_positioning.centerx
                    btn_to_draw.rect.top = arrow_y
                    btn_to_draw.draw(self.screen)
            else:
                current_answers = {}
                if self.current_question_data and "answers" in self.current_question_data and isinstance(self.current_question_data["answers"], dict) :
                    current_answers = self.current_question_data["answers"]

                for key, button in self.answer_buttons.items():
                    is_eliminated = key in self.eliminated_answers
                    clicked_button_flag = button.draw(self.screen)
                    answer_text_str = current_answers.get(key, "")
                    text_color_answer = (100, 100, 100) if is_eliminated else (255, 255, 255)
                    fonte_alternativa = self.answer_text_font
                    padding_interno_botao_x = 25
                    max_width_texto_botao = button.rect.width - (2 * padding_interno_botao_x)

                    if answer_text_str and max_width_texto_botao > 0 :
                        linhas_superficies_alt = self._wrap_text(answer_text_str, fonte_alternativa, max_width_texto_botao, text_color_answer)
                        altura_total_texto_alt_bloco = 0
                        espacamento_linhas_alt = 2
                        if linhas_superficies_alt:
                            altura_total_texto_alt_bloco = sum(surf.get_height() for surf in linhas_superficies_alt)
                            if len(linhas_superficies_alt) > 1:
                                altura_total_texto_alt_bloco += (len(linhas_superficies_alt) - 1) * espacamento_linhas_alt
                        y_linha_alt_atual = button.rect.top + (button.rect.height - altura_total_texto_alt_bloco) // 2
                        for surf_linha_alt in linhas_superficies_alt:
                            x_linha_alt = button.rect.left + (button.rect.width - surf_linha_alt.get_width()) // 2
                            self.screen.blit(surf_linha_alt, (x_linha_alt, y_linha_alt_atual))
                            y_linha_alt_atual += surf_linha_alt.get_height() + espacamento_linhas_alt

                    if not is_eliminated and clicked_button_flag and not action_taken_this_frame and self.current_question_data:
                        action_taken_this_frame = True
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                        correct_ans_key = self.current_question_data.get("correct_answer")
                        if key == correct_ans_key:
                            self.last_answer_was_correct = True # Definido aqui

                            # VERIFICA CONDIÇÃO DE VITÓRIA AQUI
                            # self.question_index é o índice da pergunta atual (0 a N-1)
                            # len(self.all_loaded_questions) é o total de perguntas na rodada (ex: 12)
                            if (self.question_index + 1) == len(self.all_loaded_questions):
                                self.game_won = True
                                self.feedback_popup_message = "PARABÉNS! Você venceu o desafio!" # Mensagem especial
                            else:
                                self.feedback_popup_message = "Parabéns! Resposta correta!"

                            # Lógica de Score (mantida)
                            score_table = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000]
                            earned = score_table[self.question_index] if self.question_index < len(score_table) else score_table[-1]
                            ranking_file = os.path.join(GAME_SCRIPT_DIR, "ranking_data.json")
                            if os.path.exists(ranking_file):
                                try:
                                    with open(ranking_file, "r", encoding="utf-8") as f: ranking_data = json.load(f)
                                except json.JSONDecodeError: ranking_data = {}
                            else: ranking_data = {}
                            current_player_name = "teste"
                            ranking_data[current_player_name] = ranking_data.get(current_player_name, 0) + earned
                            try:
                                with open(ranking_file, "w", encoding="utf-8") as f: json.dump(ranking_data, f, indent=2, ensure_ascii=False)
                            except IOError: print(f"Erro ao salvar o arquivo de ranking: {ranking_file}")
                        else: # Resposta incorreta
                            self.feedback_popup_message = f"Ops! A resposta era {correct_ans_key}."
                            self.last_answer_was_correct = False

                        self.show_feedback_popup = True
                        self.show_hint_box = False
                        for k_help in self.current_help_button_images:
                            try:
                                img = getattr(self.assets, f"botao_{k_help}0_img")
                                self.current_help_button_images[k_help] = img
                                self.help_buttons[k_help].image = img
                            except AttributeError: print(f"AVISO: Imagem de fallback 'botao_{k_help}0_img' não encontrada ao resetar ajudas.")
                        break

                if not action_taken_this_frame:
                    for name, button_help in self.help_buttons.items():
                        button_help.image = self.current_help_button_images[name]
                        clicked_help = button_help.draw(self.screen)
                        if self.help_lives_remaining > 0 and not self.help_used_for_current_question and clicked_help:
                            action_taken_this_frame = True
                            if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                            self.help_used_for_current_question = True
                            if name == "dica": self.show_hint_box = True
                            elif name == "eliminar":
                                if self.current_question_data:
                                    correct = self.current_question_data.get("correct_answer")
                                    all_keys = list(self.answer_buttons.keys())
                                    wrong_keys = [k for k in all_keys if k != correct and k not in self.eliminated_answers]
                                    num_to_eliminate = min(2, len(wrong_keys))
                                    if num_to_eliminate > 0: self.eliminated_answers.extend(random.sample(wrong_keys, num_to_eliminate))
                            elif name == "pular":
                                self.last_answer_was_correct = True
                                self.feedback_popup_message = "Você pulou a pergunta."
                                self.show_feedback_popup = True
                            for k_help_disable in self.current_help_button_images:
                                try:
                                    img_disabled = getattr(self.assets, f"botao_{k_help_disable}0_img")
                                    self.current_help_button_images[k_help_disable] = img_disabled
                                    self.help_buttons[k_help_disable].image = img_disabled
                                except AttributeError:
                                    print(f"AVISO: Imagem de fallback 'botao_{k_help_disable}0_img' não encontrada ao desabilitar ajudas.")

            if self.show_hint_box:
                self._display_hint_box()

            pygame.display.update()
            pygame.time.Clock().tick(30)
        return