from kivy.app import App, Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import abc
import threading
import number_exam


class Menu(BoxLayout, Screen):
    """
    Assign the proper screen for a given test
    set the needed extra layout
    and generate the first question.
    """
    def go_to_a_screen_test(self, screen_name):
        """"""
        app.root.current = screen_name
        screen = app.root.current_screen
        screen.design()
        screen.update_layout_with_new_question()
        screen.start_timer()


class SingleTest(BoxLayout, Screen):
    """Parent class for all the different test screens"""
    def __init__(self, **kwargs):
        __metaclass__ = abc.ABCMeta
        super(SingleTest, self).__init__(**kwargs)
        self.question: str = ''
        self.answer: str = ''
        self.score: int = 0
        self.number_of_questions: int = 0
        self.widgets: dict = {'buttons': {}}

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'design') and
                callable(subclass.design) and
                hasattr(subclass, 'update_layout_with_new_question') and
                callable(subclass.update_layout_with_new_question) or
                NotImplemented)

    @abc.abstractmethod
    def design(self):
        """Design specific layout for a given test"""
        pass

    @abc.abstractmethod
    def update_layout_with_new_question(self):
        """Generate a new question and assign it to the layout of a given test"""
        pass

    def check_answer_update_score_and_add_new_question(self, button):
        """Compare the user's answer with the expected answer"""
        if button.text == str(self.answer):
            self.score += 1
        else:
            self.score -= 1
        self.update_layout_with_new_question()

    def stop_game(self):
        """ When the timer is done, disable all buttons and show the user score"""
        for value in self.widgets['buttons'].values():
            value.disabled = True
        self.ids.score_lbl.text = f'Your score is {self.score}\n' \
                                  f'There was {self.number_of_questions} questions'

    def start_timer(self):
        """Timer to start when a test is starting"""
        timer = threading.Timer(5.0, self.stop_game)
        timer.start()

    def remove_test_layout(self):
        """
        Reset the screen and variables to its original layout/values
        Set the 'menu' screen as the current one
        """
        self.ids.boxtest.remove_widget(self.ids.boxtest.children[0])
        self.ids.score_lbl.text = ''
        self.score = 0
        self.number_of_questions = 0
        app.root.current = 'menu'


class NumbersTest(SingleTest):

    def design(self):
        h_layout = BoxLayout(orientation= 'horizontal')
        for n in range(3):
            b_name = f'button_{n+1}'
            button = Button(text='', on_release=self.check_answer_update_score_and_add_new_question,
                            font_size=80, disabled = False)
            self.widgets['buttons'][b_name] = button
            h_layout.add_widget(button)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self):
        self.question, self.answer = number_exam.get_question_and_answer()
        self.number_of_questions += 1
        # Assign the 3 numbers from the question to the text of the 3 buttons
        for i, value in enumerate(self.widgets['buttons'].values()):
            value.text = str(self.question[i])


class MainApp(App):

    def build(self):
        file = Builder.load_file('gia_screens.kv')
        return file


if __name__ == '__main__':
    app = MainApp()
    app.run()
