import random

from kivy.app import App, Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as ImgK
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from PIL import Image, ImageDraw, ImageFont

from typing import List
import abc
import time
from io import BytesIO
from dataclasses import dataclass
import threading
import gia_algo


@dataclass
class AnswerDetails:
    nb: int
    question: list
    answer: str
    answering_time: float
    correct: bool = False


functions_for_test = {'numbers':gia_algo.number_speed_and_accuracy,
                      'letters':gia_algo.perceptual_speed,
                      'rotated_r':gia_algo.spatial_visualisation,
                      'pairs':gia_algo.word_meaning,
                      'reasoning':gia_algo.reasoning}


class Menu(BoxLayout, Screen):
    """
    Assigns the proper screen for a given test
    set the needed extra layout
    and generates the first question.
    """
    def go_to_a_screen_test(self, screen_name: str):
        """"""
        app.root.current = screen_name
        screen = app.root.current_screen
        screen.screen_name = screen_name
        screen.design()
        func = functions_for_test[screen_name]
        screen.update_layout_with_new_question(func)
        screen.start_timer()


class MetaSingleTest(abc.ABCMeta,type(Screen)):
    """Combined meta class with abc and kivy"""
    pass


class AbstractSingleTest(abc.ABC, Screen, metaclass=MetaSingleTest):
    """Abstract SingleTest class to implement the new metaclass"""
    def __init__(self, **kwargs):
        super(AbstractSingleTest, self).__init__(**kwargs)


class SingleTestInterface(BoxLayout, AbstractSingleTest):
    """Interface for all the different test screens classes"""
    def __init__(self, **kwargs):
        super(SingleTestInterface, self).__init__(**kwargs)
        self.screen_name = ''
        self.question: str = ''
        self.answer: str = ''
        self.score: int = 0
        self.number_of_questions: int = 1
        self.widgets: dict = {'buttons': {}, 'labels': {}, 'images': {},'box':{}}
        self.timer: threading.Timer = None
        self.details_results: List[AnswerDetails] = []  # To store all the details of each question answered
        self.question_start_time: float = 0

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'design') and
                callable(subclass.design) and
                hasattr(subclass, 'update_layout_with_new_question') and
                callable(subclass.update_layout_with_new_question) or
                NotImplemented)

    @abc.abstractmethod
    def design(self):
        """Designs specific layout for a given test"""
        pass

    @abc.abstractmethod
    def update_layout_with_new_question(self, func):
        """Generates a new question and assigns it to the layout of a given test"""
        self.question_start_time = time.time()
        self.question,self.answer = func()

    def create_new_detail_result(self):
        detail = AnswerDetails(question= self.question,
                               answer= self.answer,
                               answering_time=time.time()-self.question_start_time,
                               nb=self.number_of_questions
                               )
        return detail

    def check_answer_update_score_and_add_new_question(self, button: Button):
        """Compares the user's answer with the expected answer"""
        # Create a new question detail
        detail = self.create_new_detail_result()
        self.details_results.append(detail)
        # Checks if answer is correct and updtes score
        if button.text == str(self.answer):
            self.score += 1
            # Set the question detail correct parameter to True
            detail.correct = True
        else:
            self.score -= 1
        # Get the proper update function to call
        func = functions_for_test[self.screen_name]
        # Generates a new question and updates the layout
        self.update_layout_with_new_question(func)
        self.number_of_questions += 1

    def stop_game(self):
        """ When the timer is done, disable all buttons and show the user score"""
        for value in self.widgets['buttons'].values():
            value.disabled = True
        self.ids.score_lbl.text = f'Your score is {self.score}\n' \
                                  f'There was {self.number_of_questions} questions'
        for detail in self.details_results:
            print(f'Question: {detail.nb} was {detail.correct} in {round(detail.answering_time,1)} s')

    def start_timer(self):
        """Timer to start when a test is starting"""
        self.timer = threading.Timer(180, self.stop_game)
        self.timer.start()

    def remove_test_layout(self):
        """
        Reset the screen and variables to their original layout/values
        Set the 'menu' screen as the current one
        """
        self.timer.cancel()
        # Loop through the range of the length of children because
        # when looping through the children, some were missed and
        # I couldn't figure out why
        for n in range(len(self.ids.boxtest.children)):
            self.ids.boxtest.remove_widget(self.ids.boxtest.children[0])
        self.ids.score_lbl.text = ''
        self.score = 0
        self.number_of_questions = 1
        app.root.current = 'menu'


class NumbersTest(SingleTestInterface):

    def design(self):
        layout_for_3_choices(self)

    def update_layout_with_new_question(self, func):
        super().update_layout_with_new_question(func)
        update_layout_for_3_choices(self)


class LettersTest(SingleTestInterface):

    def design(self):
        h_layout = BoxLayout(orientation='vertical',
                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             size_hint=(0.8, 0.7))
        grid = GridLayout(cols=4,
                          spacing=30,
                          size_hint=(1, 0.5))
        for n in range(8):
            lbl = Label(text='',
                        font_size=60)
            grid.add_widget(lbl)
            self.widgets['labels'][f'letter_{str(n)}'] = lbl
        answers_line = BoxLayout(orientation='horizontal',
                                 size_hint=(1, 0.4))
        for n in range(5):
            a_btn = Button(text=str(n),
                           on_release=self.check_answer_update_score_and_add_new_question,
                           font_size=50,
                           disabled=False)
            answers_line.add_widget(a_btn)
            self.widgets['buttons'][f'answer_{str(n)}']=a_btn
        h_layout.add_widget(grid)
        h_layout.add_widget(Label(size_hint=(1, 0.2)))
        h_layout.add_widget(answers_line)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self, func):
        super().update_layout_with_new_question(func)
        for label, letter in zip(self.widgets['labels'],self.question):
            self.widgets['labels'][label].text = letter


class RTest(SingleTestInterface):

    def design(self):
        h_layout = BoxLayout(orientation='vertical',
                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             size_hint=(0.8, 0.8))
        grid = GridLayout(cols=2,
                          size_hint=(0.5, 0.8),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        for n in range(4):
            source = make_r_image(0, 0)
            img = ImgK()
            img.texture = source.texture
            grid.add_widget(img)
            self.widgets['images'][f'image_{str(n)}'] = img
        h_layout.add_widget(grid)
        answers_line = BoxLayout(orientation='horizontal',
                                 size_hint=(0.8, 0.3),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        for n in range(3):
            a_btn = Button(text=str(n),
                           on_release=self.check_answer_update_score_and_add_new_question,
                           font_size=50,
                           disabled=False)
            answers_line.add_widget(a_btn)
            self.widgets['buttons'][f'answer_{str(n)}']=a_btn
        h_layout.add_widget(Label(size_hint=(1,0.2)))
        h_layout.add_widget(answers_line)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self, func):
        super().update_layout_with_new_question(func)
        R_data =[self.question[0][0],self.question[1][0],self.question[0][1],self.question[1][1]]
        for data, image in zip(R_data,self.widgets['images'].values()):
            source = make_r_image(data[0], data[1])
            image.texture = source.texture


class PairsTest(SingleTestInterface):

    def design(self):
        layout_for_3_choices(self)

    def update_layout_with_new_question(self, func):
        super().update_layout_with_new_question(func)
        update_layout_for_3_choices(self)


class ReasoningTest(SingleTestInterface):

    def design(self):
        h_layout = BoxLayout(orientation='vertical',
                             pos_hint={'center_x': 0.5, 'center_y': 0.7},
                             size_hint=(0.8, 0.8)
                             )
        fact_question = Label(text="test",
                              font_size=40,
                              size_hint=(0.8, 0.8),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5}
                              )
        self.widgets['labels']['fact'] = fact_question

        # Layout which holds either the See question button
        # or the 2 answer buttons with names
        button_layout = BoxLayout(size_hint=(0.4, 0.5),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}
                                  )
        self.widgets['box']['buttons'] = button_layout
        # Create buttons but don't add them to the layout yet.
        # Only when update_layout_with_new_question is called
        see_question = Button(text='Get question',on_release=self.get_question, font_size = 30
                              )
        name1 = Button(text='', on_release=self.check_answer_update_score_and_add_new_question, font_size = 40, )
        name2 = Button(text='', on_release=self.check_answer_update_score_and_add_new_question, font_size = 40, )
        self.widgets['buttons']['see_question']=see_question
        self.widgets['buttons']['name1']=name1
        self.widgets['buttons']['name2']=name2
        # Add the label and buttons layout to the main layout
        h_layout.add_widget(fact_question)
        h_layout.add_widget(button_layout)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self, func):
        super().update_layout_with_new_question(func)
        self.widgets['labels']['fact'].text = self.question[0]
        # Remove the answers buttons
        self.widgets['box']['buttons'].remove_widget(self.widgets['buttons']['name1'])
        self.widgets['box']['buttons'].remove_widget(self.widgets['buttons']['name2'])
        # Add the See question button
        self.widgets['box']['buttons'].add_widget(self.widgets['buttons']['see_question'])

    def get_question(self, d):
        # Shuffle the 2 answer names so that the first one named in the fact
        # is not always the first choice
        shuffled_names = self.question[2]
        random.shuffle(shuffled_names)
        # Replace the fact text by the question text
        self.widgets['labels']['fact'].text = self.question[1]
        # Remove the See question button
        self.widgets['box']['buttons'].size_hint = (0.8, 0.5)
        self.widgets['box']['buttons'].remove_widget(self.widgets['buttons']['see_question'])
        # Set the text on the answer buttons
        self.widgets['buttons']['name1'].text = shuffled_names[0]
        self.widgets['buttons']['name2'].text = shuffled_names[1]
        # Add the 2 answer buttons to the layout
        self.widgets['box']['buttons'].add_widget(self.widgets['buttons']['name1'])
        self.widgets['box']['buttons'].add_widget(self.widgets['buttons']['name2'])


def layout_for_3_choices(screen):
    """Generates main layout for 3 choices questions"""
    h_layout = BoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                         size_hint=(0.6, 0.6))
    for n in range(3):
        b_name = f'button_{n+1}'
        button = Button(text='',
                        on_release=screen.check_answer_update_score_and_add_new_question,
                        font_size=30,
                        disabled=False)
        screen.widgets['buttons'][b_name] = button
        h_layout.add_widget(button)
    screen.ids.boxtest.add_widget(h_layout)


def update_layout_for_3_choices(screen):
    """Assign the 3 numbers from the question to the text of the 3 buttons"""
    for i, value in enumerate(screen.widgets['buttons'].values()):
        value.text = str(screen.question[i])


def make_r_image(side, angle):
    """Generates a PIL Image of a drawn R with a given side and angle"""
    # Define text font
    fnt = ImageFont.truetype('arial.ttf', 85)
    # Create a new PIL image
    image = Image.new(mode = "RGB", size = (150,150), color = "white")
    # Draw a black R on the image
    draw = ImageDraw.Draw(image)
    draw.text((40, 40), "R", font=fnt, fill='black',align='center',stroke_width=1,
              stroke_fill="black")
    # Rotate the image
    image = image.rotate(angle)
    # Flip the image horizontally if needed
    if side == 1:
        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
    # Convert the image to bytes
    data = BytesIO()
    image.save(data, format='png')
    data.seek(0)
    # Generates a Kivy CoreImage
    image = CoreImage(BytesIO(data.read()), ext='png')
    return image


class MainApp(App):

    def build(self):
        print(Window.size)
        file = Builder.load_file('gia_screens.kv')
        return file


if __name__ == '__main__':
    app = MainApp()
    app.run()
