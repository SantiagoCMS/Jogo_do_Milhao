import pygame
from jogo.button import Button
import random
import sqlite3
import json
import os

GAME_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME_FOR_GAME = os.path.join(GAME_SCRIPT_DIR, "quiz_banco.db")

class GameScreen:
    """Classe que gerencia a tela principal do quiz com perguntas e interações."""

    def __init__(self, screen, assets, selected_level, selected_subjects_list):
        self.screen = screen  # Surface do pygame onde tudo será desenhado
        self.assets = assets  # Recursos gráficos e fontes usados na tela
        self.running_show_loop = True  # Controle do loop principal da tela
        self.last_arrow_click_time = 0  # Tempo do último clique nas setas (para evitar cliques rápidos demais)
        self.arrow_click_delay = 500  # Delay em milissegundos entre cliques nas setas

        # Botões para as respostas, posicionados na tela
        self.answer_buttons = {
            "A": Button(40, 280, assets.answer_a_img),
            "B": Button(40, 380, assets.answer_b_img),
            "C": Button(40, 480, assets.answer_c_img),
            "D": Button(40, 580, assets.answer_d_img),
        }

        # Botões para ajudas (pular pergunta, dica e eliminar resposta)
        self.help_buttons = {
            "pular": Button(560, 620, assets.botao_pular3_img),
            "dica": Button(730, 620, assets.botao_dica3_img),
            "eliminar": Button(900, 620, assets.botao_eliminar3_img),
        }

        self.help_used_for_current_question = False  # Indica se já usou ajuda na pergunta atual
        self.current_question_data = None  # Dados da pergunta atual
        self.show_feedback_popup = False  # Controle para mostrar o popup de feedback
        self.feedback_popup_message = ""  # Texto do popup de feedback
        self.popup_font = assets.small_font  # Fonte para o popup
        self.show_hint_box = False  # Controle para mostrar caixa de dica
        self.hint_font = assets.small_font  # Fonte para as dicas
        self.eliminated_answers = []  # Respostas eliminadas pela ajuda "eliminar"
        self.question_index = 0  # Índice da pergunta atual na lista
        self.last_answer_was_correct = False  # Guarda se a última resposta estava certa
        self.help_lives_remaining = 3  # Quantidade de "vidas" de ajuda restantes

        # Armazena as imagens atuais dos botões de ajuda (variam conforme vidas restantes)
        self.current_help_button_images = {
            "pular": assets.botao_pular3_img,
            "dica": assets.botao_dica3_img,
            "eliminar": assets.botao_eliminar3_img
        }

        self.popup_rect_for_positioning = None  # Retângulo para posicionar o popup de feedback
        self.right_arrow_button = Button(0, 0, assets.right_arrow_img)  # Botão seta direita (posição definida depois)
        self.left_arrow_button = Button(0, 0, assets.left_arrow_img)  # Botão seta esquerda (posição definida depois)

        # Carrega perguntas do banco SQLite baseado no nível e matérias selecionadas
        self.all_loaded_questions = self._load_questions_from_sqlite(DB_FILENAME_FOR_GAME, selected_level, selected_subjects_list)

        # Caso não carregue perguntas do banco, usa perguntas padrão de fallback
        if not self.all_loaded_questions:
            self.all_loaded_questions = [{
                "text": "Erro: Perguntas não carregadas!",
                "answers": {"A": "-", "B": "-", "C": "-", "D": "-"},
                "correct_answer": "A",
                "tip": "Verifique o arquivo quiz_banco.db ou o código."
            }]

        self.question_text_font = self.assets.medium_font  # Fonte para o texto da pergunta
        self.answer_text_font = getattr(self.assets, 'answer_font', self.assets.small_font)  # Fonte para as respostas (fallback)

        self.game_won = False  # Estado que indica se o jogador já venceu o quiz


    def _get_placeholder_questions(self):
        # Perguntas usadas como fallback se o banco não carregar
        return [
            {"text": "Qual linguagem o Pygame usa?", "answers": {"A": "Python", "B": "Java", "C": "C#", "D": "Lua"}, "correct_answer": "A", "tip": "É uma linguagem de script muito popular."},
            {"text": "Qual o resultado de 2 elevado a 3?", "answers": {"A": "5", "B": "6", "C": "8", "D": "9"}, "correct_answer": "C", "tip": "Multiplique 2 por ele mesmo, 3 vezes."},
            {"text": "Qual a cor do cavalo branco de Napoleão?", "answers": {"A": "Preto", "B": "Marrom", "C": "Branco", "D": "Malhado"}, "correct_answer": "C", "tip": "A pergunta já contém a resposta!"}
        ]

    def _load_questions_from_sqlite(self, db_path, target_level, target_subjects_list):
        loaded_questions = []
        if not os.path.exists(db_path):
            # Se o arquivo do banco não existe, retorna perguntas padrão
            return self._get_placeholder_questions()
        if not target_level or not target_subjects_list:
            # Se não recebeu nível ou matérias, retorna perguntas padrão
            return self._get_placeholder_questions()

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
        cursor = conn.cursor()

        query_base = "SELECT id, text, answer_a, answer_b, answer_c, answer_d, correct_answer, tip, subject, level FROM questions"
        conditions = ["level = ?"]
        params = [target_level]

        if target_subjects_list:
            # Prepara placeholders "?" para os parâmetros SQL e adiciona a condição de matérias
            placeholders = ", ".join(["?"] * len(target_subjects_list))
            conditions.append(f"subject IN ({placeholders})")
            params.extend(target_subjects_list)

        query = f"{query_base} WHERE {' AND '.join(conditions)}"
        cursor.execute(query, tuple(params))
        db_rows = cursor.fetchall()

        for row in db_rows:
            # Monta lista de perguntas com dados do banco
            loaded_questions.append({
                "id": row["id"], "text": row["text"],
                "answers": {"A": row["answer_a"], "B": row["answer_b"], "C": row["answer_c"], "D": row["answer_d"]},
                "correct_answer": row["correct_answer"], "tip": row["tip"], "subject": row["subject"], "level": row["level"]
            })

        if loaded_questions:
            random.shuffle(loaded_questions)  # Embaralha as perguntas
            if len(loaded_questions) > 12:
                loaded_questions = loaded_questions[:12]  # Limita a 12 perguntas

        conn.close()

        if not loaded_questions:
            # Se nenhuma pergunta foi carregada, retorna as padrão
            return self._get_placeholder_questions()

        return loaded_questions

    def _setup_for_new_question(self):
        # Prepara dados para exibir uma nova pergunta
        if not self.all_loaded_questions:
            # Se não tem perguntas, define um erro para mostrar
            self.current_question_data = {"text": "ERRO AO CARREGAR PERGUNTAS!", "answers": {"A": "Verifique console", "B": "-", "C": "-", "D": "-"}, "correct_answer": "A", "tip": "Problema com quiz_banco.db"}
            self.show_feedback_popup = False
            self.show_hint_box = False
            self.eliminated_answers = []
            self.last_answer_was_correct = False
            self.help_used_for_current_question = False

            # Atualiza imagens dos botões de ajuda para 0 vidas restantes
            life_suffix = "0"
            for name_key in self.help_buttons:
                image = getattr(self.assets, f"botao_{name_key}{life_suffix}_img")
                if image:
                    self.current_help_button_images[name_key] = image
                    self.help_buttons[name_key].image = image
            return

        # Se o jogo foi vencido ou todas as perguntas foram respondidas, não faz nada
        if self.game_won or self.question_index >= len(self.all_loaded_questions):
            return

        # Se usou ajuda e acertou a pergunta, reduz as vidas restantes de ajuda
        if self.last_answer_was_correct and self.help_used_for_current_question:
            if self.help_lives_remaining > 0:
                self.help_lives_remaining -= 1

        idx = self.question_index
        self.current_question_data = self.all_loaded_questions[idx]

        self.show_feedback_popup = False
        self.show_hint_box = False
        self.eliminated_answers = []
        self.last_answer_was_correct = False
        self.help_used_for_current_question = False

        # Atualiza imagens dos botões de ajuda conforme as vidas restantes
        life_suffix = str(self.help_lives_remaining)
        for name_key in self.help_buttons:
            image = getattr(self.assets, f"botao_{name_key}{life_suffix}_img", getattr(self.assets, f"botao_{name_key}0_img", None))
            if image:
                self.current_help_button_images[name_key] = image
                self.help_buttons[name_key].image = image

    def _display_win_screen(self):
        # Exibe a tela de vitória e aguarda ação do jogador para sair dela
        parabens_img_surface = self.assets.parabens_img
        parabens_rect = parabens_img_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(self.assets.background, (0,0))  # Desenha fundo da tela
        self.screen.blit(parabens_img_surface, parabens_rect)  # Desenha imagem de parabéns

        pygame.display.update()

        waiting_for_input_to_exit_win_screen = True

        # Limpa eventos antigos para evitar sair imediatamente
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        pygame.event.clear(pygame.KEYDOWN)

        while waiting_for_input_to_exit_win_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False  # Fecha o jogo
                    waiting_for_input_to_exit_win_screen = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_input_to_exit_win_screen = False  # Sai da tela de vitória ao clicar ou teclar

            if not self.running_show_loop:
                break

            pygame.time.Clock().tick(30)  # Controla o FPS para não travar o programa

        self.running_show_loop = False  # Fecha a tela do jogo após a vitória

    def _wrap_text(self, text, font, max_width, text_color=(255,255,255)):
        # Quebra texto em múltiplas linhas para caber dentro da largura máxima definida
        rendered_lines = []
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            words = paragraph.split(' ')
            current_line_str = ""
            for i, word in enumerate(words):
                # Tenta juntar a palavra atual com a linha para verificar se cabe no espaço
                line_candidate_str = current_line_str + (" " if current_line_str else "") + word
                candidate_width = font.render(line_candidate_str, True, text_color).get_width()
                word_width_alone = font.render(word, True, text_color).get_width()

                if candidate_width <= max_width:
                    current_line_str = line_candidate_str
                else:
                    # Se não cabe, salva a linha atual e começa uma nova
                    if current_line_str:
                        rendered_lines.append(font.render(current_line_str, True, text_color))
                    current_line_str = word
                    # Se a palavra sozinha não cabe, adiciona ela como linha independente para evitar loop
                    if word_width_alone > max_width and current_line_str == word:
                        rendered_lines.append(font.render(current_line_str, True, text_color))
                        current_line_str = ""
            if current_line_str:
                rendered_lines.append(font.render(current_line_str, True, text_color))
        return rendered_lines

    def _display_feedback_popup(self):
        if not self.show_feedback_popup:
            return

        # Define tamanho e posição do retângulo do popup centralizado
        w, h = 450, 150
        x = (self.screen.get_width() - w) // 2
        y = (self.screen.get_height() - h) // 2
        self.popup_rect_for_positioning = pygame.Rect(x, y, w, h)

        # Desenha o retângulo branco e a borda colorida
        pygame.draw.rect(self.screen, (255, 255, 255), self.popup_rect_for_positioning)
        pygame.draw.rect(self.screen, (0, 208, 171), self.popup_rect_for_positioning, 5)

        # Renderiza o texto do feedback e centraliza dentro do popup
        text_surface = self.popup_font.render(self.feedback_popup_message, True, (0, 208, 171))
        text_rect = text_surface.get_rect(center=self.popup_rect_for_positioning.center)
        self.screen.blit(text_surface, text_rect)

    def _display_hint_box(self):
        if not self.show_hint_box or not self.current_question_data:
            return
        hint = self.current_question_data.get("tip", "Dica não disponível.")
        tip_image = getattr(self.assets, 'tip_box_img', None)
        w, h = tip_image.get_size() if tip_image else (250, 120)
        x, y = self.screen.get_width() - w - 50, 270

        if tip_image:
            self.screen.blit(tip_image, (x, y))
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, w, h))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, w, h), 2)

        padding, max_width = 30, w - 60
        words = hint.split(' ')
        lines, line = [], ""

        for word in words:
            test_line = line + word + " "
            if self.hint_font.render(test_line, True, (0, 0, 0)).get_width() <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())

        for i, txt in enumerate(lines):
            surf = self.hint_font.render(txt, True, (255, 255, 255))  # texto branco para contraste
            self.screen.blit(surf, (x + padding, y + padding + i * self.hint_font.get_linesize()))


    def show(self):
        self._setup_for_new_question()

        # Espera mouse soltar clique antes de começar
        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False
                    return
            pygame.time.wait(10)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        self.running_show_loop = True
        while self.running_show_loop:

            # Se venceu o jogo, mostra tela de vitória e sai do loop
            if self.game_won:
                self._display_win_screen()
                continue

            action_taken_this_frame = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False

                # Feedback popup: clique nas setas para avançar ou voltar
                if self.show_feedback_popup and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_arrow_click_time >= self.arrow_click_delay:
                        action_taken_this_frame = True

                        if self.last_answer_was_correct and self.right_arrow_button.rect.collidepoint(mouse_pos):
                            if hasattr(self.assets, 'click_sound'):
                                self.assets.click_sound.play()
                            pygame.event.clear(pygame.MOUSEBUTTONDOWN)

                            if self.game_won:
                                self.show_feedback_popup = False
                            else:
                                self.question_index += 1
                                if self.question_index < len(self.all_loaded_questions):
                                    self._setup_for_new_question()
                                else:
                                    self.game_won = True
                                self.show_feedback_popup = False
                            self.last_arrow_click_time = current_time

                        elif (not self.last_answer_was_correct and
                            self.left_arrow_button.rect.collidepoint(mouse_pos)):
                            if hasattr(self.assets, 'click_sound'):
                                self.assets.click_sound.play()
                            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                            self.running_show_loop = False
                            self.show_feedback_popup = False
                            self.last_arrow_click_time = current_time

            if not self.running_show_loop:
                break

            # Desenha background e caixa da pergunta
            self.screen.blit(self.assets.background, (0, 0))
            box_x = (self.screen.get_width() - 968) // 2
            self.screen.blit(self.assets.question_box_img, (box_x, 20))

            # Renderiza pergunta com quebra de linha e centralização
            question_text = self.current_question_data.get("text", "...") if self.current_question_data else "..."
            padding_x = 45
            max_width = 968 - 2 * padding_x
            linhas = self._wrap_text(question_text, self.question_text_font, max_width)
            y_atual = 20 + 25
            espacamento = 4
            for linha in linhas:
                x_linha = box_x + padding_x + (max_width - linha.get_width()) // 2
                self.screen.blit(linha, (x_linha, y_atual))
                y_atual += linha.get_height() + espacamento

            if self.show_feedback_popup:
                self._display_feedback_popup()
                if self.popup_rect_for_positioning:
                    arrow_y = self.popup_rect_for_positioning.bottom + 20
                    btn = self.right_arrow_button if self.last_answer_was_correct else self.left_arrow_button
                    btn.rect.centerx = self.popup_rect_for_positioning.centerx
                    btn.rect.top = arrow_y
                    btn.draw(self.screen)

            else:
                # Renderiza respostas e trata clique
                current_answers = self.current_question_data.get("answers", {}) if self.current_question_data else {}

                for key, btn in self.answer_buttons.items():
                    eliminado = key in self.eliminated_answers
                    clicado = btn.draw(self.screen)
                    texto = current_answers.get(key, "")
                    cor_texto = (100, 100, 100) if eliminado else (255, 255, 255)

                    max_largura = btn.rect.width - 50
                    linhas_alt = self._wrap_text(texto, self.answer_text_font, max_largura, cor_texto)

                    altura_total = sum(linha.get_height() for linha in linhas_alt) + (len(linhas_alt) - 1) * 2 if linhas_alt else 0
                    y_linha = btn.rect.top + (btn.rect.height - altura_total) // 2

                    for surf_linha in linhas_alt:
                        x_linha = btn.rect.left + (btn.rect.width - surf_linha.get_width()) // 2
                        self.screen.blit(surf_linha, (x_linha, y_linha))
                        y_linha += surf_linha.get_height() + 2

                    if not eliminado and clicado and not action_taken_this_frame and self.current_question_data:
                        action_taken_this_frame = True
                        if hasattr(self.assets, 'click_sound'):
                            self.assets.click_sound.play()

                        correto = self.current_question_data.get("correct_answer")
                        if key == correto:
                            self.last_answer_was_correct = True
                            if (self.question_index + 1) == len(self.all_loaded_questions):
                                self.game_won = True
                                self.feedback_popup_message = "PARABÉNS! Você venceu o desafio!"
                            else:
                                self.feedback_popup_message = "Parabéns! Resposta correta!"

                            score_table = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000]
                            earned = score_table[self.question_index] if self.question_index < len(score_table) else score_table[-1]

                            ranking_file = os.path.join(GAME_SCRIPT_DIR, "ranking_data.json")
                            ranking_data = {}
                            if os.path.exists(ranking_file):
                                with open(ranking_file, "r", encoding="utf-8") as f:
                                    ranking_data = json.load(f)

                            current_player_name = "teste"
                            ranking_data[current_player_name] = ranking_data.get(current_player_name, 0) + earned
                            with open(ranking_file, "w", encoding="utf-8") as f:
                                json.dump(ranking_data, f, indent=2, ensure_ascii=False)

                        else:
                            self.feedback_popup_message = f"Ops! A resposta era {correto}."
                            self.last_answer_was_correct = False

                        self.show_feedback_popup = True
                        self.show_hint_box = False

                        # Reseta botões de ajuda
                        for k in self.current_help_button_images:
                            img = getattr(self.assets, f"botao_{k}0_img")
                            self.current_help_button_images[k] = img
                            self.help_buttons[k].image = img
                        break

                # Tratamento dos botões de ajuda (dica, eliminar, pular)
                if not action_taken_this_frame:
                    for nome, btn_ajuda in self.help_buttons.items():
                        btn_ajuda.image = self.current_help_button_images[nome]
                        clicado_ajuda = btn_ajuda.draw(self.screen)

                        if self.help_lives_remaining > 0 and not self.help_used_for_current_question and clicado_ajuda:
                            action_taken_this_frame = True
                            if hasattr(self.assets, 'click_sound'):
                                self.assets.click_sound.play()
                            self.help_used_for_current_question = True

                            if nome == "dica":
                                self.show_hint_box = True

                            elif nome == "eliminar":
                                if self.current_question_data:
                                    correto = self.current_question_data.get("correct_answer")
                                    todas_chaves = list(self.answer_buttons.keys())
                                    erradas = [k for k in todas_chaves if k != correto and k not in self.eliminated_answers]
                                    qtd_eliminar = min(2, len(erradas))
                                    if qtd_eliminar > 0:
                                        self.eliminated_answers.extend(random.sample(erradas, qtd_eliminar))

                            elif nome == "pular":
                                self.last_answer_was_correct = True
                                self.feedback_popup_message = "Você pulou a pergunta."
                                self.show_feedback_popup = True

                            # Reseta imagens dos botões de ajuda
                            for k in self.current_help_button_images:
                                img_desabilitada = getattr(self.assets, f"botao_{k}0_img")
                                self.current_help_button_images[k] = img_desabilitada
                                self.help_buttons[k].image = img_desabilitada

            if self.show_hint_box:
                self._display_hint_box()

            pygame.display.update()
            pygame.time.Clock().tick(30)
