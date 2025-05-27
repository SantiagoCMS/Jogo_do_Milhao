import pygame
from button import Button
import random

class GameScreen:
    """Tela principal do quiz com perguntas e interações."""

    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.running_show_loop = True

        self.answer_buttons = {
            "A": Button(40, 240, assets.answer_a_img),
            "B": Button(40, 340, assets.answer_b_img),
            "C": Button(40, 440, assets.answer_c_img),
            "D": Button(40, 540, assets.answer_d_img),
        }

        self.help_buttons = {
            "pular": Button(500, 620, assets.botao_pular3_img),
            "dica": Button(700, 620, assets.botao_dica3_img),
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

        self.placeholder_questions = [
            {
                "text": "Qual linguagem o Pygame usa?",
                "answers": {"A": "Python", "B": "Java", "C": "C#", "D": "Lua"},
                "correct_answer": "A",
                "tip": "É uma linguagem de script muito popular."
            },
            {
                "text": "Qual o resultado de 2 elevado a 3?",
                "answers": {"A": "5", "B": "6", "C": "8", "D": "9"},
                "correct_answer": "C",
                "tip": "Multiplique 2 por ele mesmo, 3 vezes."
            },
            {
                "text": "Qual a cor do cavalo branco de Napoleão?",
                "answers": {"A": "Preto", "B": "Marrom", "C": "Branco", "D": "Malhado"},
                "correct_answer": "C",
                "tip": "A pergunta já contém a resposta!"
            }
        ]

    def _setup_for_new_question(self):
        if self.last_answer_was_correct and self.help_used_for_current_question:
            if self.help_lives_remaining > 0:
                self.help_lives_remaining -= 1

        idx = self.question_index % len(self.placeholder_questions)
        self.current_question_data = self.placeholder_questions[idx]

        self.show_feedback_popup = False
        self.show_hint_box = False
        self.eliminated_answers = []
        self.last_answer_was_correct = False
        self.help_used_for_current_question = False

        life_suffix = str(self.help_lives_remaining)
        for name_key in self.help_buttons:
            try:
                image = getattr(self.assets, f"botao_{name_key}{life_suffix}_img")
            except AttributeError:
                image = getattr(self.assets, f"botao_{name_key}0_img", None)
                if self.help_lives_remaining > 0:
                    print(f"AVISO: Imagem 'botao_{name_key}{life_suffix}_img' não encontrada. Usando fallback.")
            if image:
                self.current_help_button_images[name_key] = image
                self.help_buttons[name_key].image = image
            else:
                print(f"AVISO CRÍTICO: Nenhuma imagem encontrada para {name_key}.")

    def _display_feedback_popup(self):
        if not self.show_feedback_popup: return
        w, h = 450, 150
        x = (self.screen.get_width() - w) // 2
        y = (self.screen.get_height() - h) // 2
        self.popup_rect_for_positioning = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255, 255, 255), self.popup_rect_for_positioning)
        pygame.draw.rect(self.screen, (0, 208, 171), self.popup_rect_for_positioning, 5)
        text_surface = self.popup_font.render(self.feedback_popup_message, True, (0, 208, 171))
        text_rect = text_surface.get_rect(center=self.popup_rect_for_positioning.center)
        self.screen.blit(text_surface, text_rect)

    def _display_hint_box(self):
        if not self.show_hint_box or not self.current_question_data: return
        hint = self.current_question_data.get("tip", "Dica não disponível.")
        tip_image = getattr(self.assets, 'tip_box_img', None)
        w, h = tip_image.get_size() if tip_image else (250, 120)
        x, y = self.screen.get_width() - w - 50, 240
        if tip_image:
            self.screen.blit(tip_image, (x, y))
        else:
            pygame.draw.rect(self.screen, (200,200,200), (x,y,w,h))
            pygame.draw.rect(self.screen, (0,0,0), (x,y,w,h), 2)
        padding, max_width = 30, w - 60
        words, lines, line = hint.split(' '), [], ""
        for word in words:
            test_line = line + word + " "
            if self.hint_font.render(test_line, True, (0,0,0)).get_width() <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        for i, txt in enumerate(lines):
            surf = self.hint_font.render(txt, True, (255,255,255))
            self.screen.blit(surf, (x + padding, y + padding + i * self.hint_font.get_linesize()))

    def show(self):
        self._setup_for_new_question()

        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False
                    return
            pygame.time.wait(10)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        self.running_show_loop = True

        while self.running_show_loop:
            action_taken_this_frame = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_show_loop = False

                if self.show_feedback_popup and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action_taken_this_frame = True
                    clicked_on_arrow = False
                    if self.last_answer_was_correct:
                        if self.right_arrow_button.rect.collidepoint(mouse_pos):
                            if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                            self.question_index += 1
                            self._setup_for_new_question()
                            clicked_on_arrow = True
                    else:
                        if self.left_arrow_button.rect.collidepoint(mouse_pos):
                            if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                            pygame.time.wait(200)  # EVITA CLIQUE DUPLO
                            self.running_show_loop = False
                            clicked_on_arrow = True
                    if clicked_on_arrow:
                        self.show_feedback_popup = False
                        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            if not self.running_show_loop: break

            self.screen.blit(self.assets.background, (0, 0))
            box_x = (self.screen.get_width() - 968) // 2
            self.screen.blit(self.assets.question_box_img, (box_x, 20))

            question_text = self.current_question_data.get("text", "") if self.current_question_data else ""
            txt_surf = self.assets.medium_font.render(question_text, True, (255, 255, 255))
            text_x = box_x + (968 - txt_surf.get_width()) // 2
            self.screen.blit(txt_surf, (text_x, 20 + (208 - txt_surf.get_height()) // 2 - 30))

            if self.show_feedback_popup:
                self._display_feedback_popup()
                if self.popup_rect_for_positioning:
                    arrow_y = self.popup_rect_for_positioning.bottom + 20
                    btn = self.right_arrow_button if self.last_answer_was_correct else self.left_arrow_button
                    btn.rect.centerx = self.popup_rect_for_positioning.centerx
                    btn.rect.top = arrow_y
                    btn.draw(self.screen)
            else:
                for key, button in self.answer_buttons.items():
                    if key in self.eliminated_answers:
                        button.draw(self.screen)
                        continue
                    clicked = button.draw(self.screen)
                    answer_text = self.current_question_data["answers"].get(key, "")
                    if answer_text:
                        txt_surf = self.assets.small_font.render(answer_text, True, (255, 255, 255))
                        self.screen.blit(txt_surf, txt_surf.get_rect(center=button.rect.center))
                    if clicked and not action_taken_this_frame:
                        action_taken_this_frame = True
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                        correct = self.current_question_data.get("correct_answer")
                        if key == correct:
                            self.feedback_popup_message = "Parabéns! Resposta correta!"
                            self.last_answer_was_correct = True
                            score_table = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000]
                            earned = score_table[self.question_index] if self.question_index < len(score_table) else 0
                            import json, os
                            ranking_file = "ranking_data.json"
                            if os.path.exists(ranking_file):
                                with open(ranking_file, "r", encoding="utf-8") as f:
                                    ranking_data = json.load(f)
                            else:
                                ranking_data = {}
                            ranking_data["teste"] = ranking_data.get("teste", 0) + earned
                            with open(ranking_file, "w", encoding="utf-8") as f:
                                json.dump(ranking_data, f, indent=2)
                        else:
                            self.feedback_popup_message = f"Ops! A resposta era {correct}."
                            self.last_answer_was_correct = False
                        self.show_feedback_popup = True
                        self.show_hint_box = False
                        for k in self.current_help_button_images:
                            try:
                                img = getattr(self.assets, f"botao_{k}0_img")
                                self.current_help_button_images[k] = img
                                self.help_buttons[k].image = img
                            except AttributeError:
                                print(f"AVISO: Imagem 'botao_{k}0_img' não encontrada.")
                        break

                if not action_taken_this_frame:
                    for name, button in self.help_buttons.items():
                        button.image = self.current_help_button_images[name]
                        clicked = button.draw(self.screen)
                        if self.help_lives_remaining > 0 and not self.help_used_for_current_question and clicked:
                            action_taken_this_frame = True
                            if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                            if name == "dica":
                                self.show_hint_box = True
                            elif name == "eliminar":
                                correct = self.current_question_data.get("correct_answer")
                                all_keys = list(self.answer_buttons.keys())
                                wrong_keys = [k for k in all_keys if k != correct and k not in self.eliminated_answers]
                                self.eliminated_answers.extend(random.sample(wrong_keys, min(2, len(wrong_keys))))
                            elif name == "pular":
                                self.last_answer_was_correct = True
                                self.feedback_popup_message = "Você pulou a pergunta."
                                self.show_feedback_popup = True
                            self.help_used_for_current_question = True
                            for k in self.current_help_button_images:
                                try:
                                    img = getattr(self.assets, f"botao_{k}0_img")
                                    self.current_help_button_images[k] = img
                                    self.help_buttons[k].image = img
                                except AttributeError:
                                    print(f"AVISO: Imagem 'botao_{k}0_img' não encontrada.")
                            break

                if self.show_hint_box:
                    self._display_hint_box()

            pygame.display.update()