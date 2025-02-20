'''
Author: Krish Rajani
Date: 8th April 2024
this code implements a carousel using a circular doubly linked list
and displays emojis obtained from a json file, in the carousel
'''


import json
import os
import time
from circular_dlinked_list import CircularDoublyLinkedList
from art import frames


class Carousel:
    def __init__(self, json_file):
        self.emojis = self.load_emojis(json_file)
        self.current_node = None
        self.list = CircularDoublyLinkedList()

    def load_emojis(self, json_file):
        '''
        read data from json file and store it in a dictionary using json.load
        '''
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)#store data in a dictionary

    def add_node(self):
        '''
        allows the user to add a new node to the circular doubly linked list
        that is used to display the carousel
        '''
        emoji_name = input("what do you want to add? ").lower()#prompt the user to input an emoji name
        emoji_data = self.find_emoji(emoji_name)
    
        if emoji_data:
            if self.list.is_empty():
                self.list.add_node(emoji_data)
                self.current_node = self.list.get_current_node()
            else:
                position = input("on which side do you want to add the emoji frame? (left/right): ").upper()
                if position == 'LEFT':#if the user types l, the carousel moves left
                    self.list.move_left()
                    self.list.add_node(emoji_data)
                    self.current_node = self.list.get_current_node()
                    print(frames[8])  #display adding left animation
                    time.sleep(1)  #delay of 2 second
                elif position == 'RIGHT':#if the user types r, the carousel moves right
                    self.list.move_right()
                    self.list.add_node(emoji_data)
                    self.current_node = self.list.get_current_node()
                    print(frames[5])  #display adding right animation
                    time.sleep(1) #delay of 1 second
                else:
                    print("Invalid input. Please enter 'LEFT' or 'RIGHT'.")
                    return
            os.system('cls' if os.name == 'nt' else 'clear') #clears the screen after the inputs
            self.display_carousel()  #display the new carousel
        else:
            print("Emoji not found. Please try again.")
            
    def find_emoji(self, name):
        '''
        ierate the dictionary we created earlier and find
        the emoji that was types in by the user
        '''
        for category in self.emojis:#iterate through the emojis
            if name in category['emojis']:
                return {
                    'class': category['class'],
                    'name': name,
                    'symbol': category['emojis'][name]
                }
        return None

    def delete_node(self):
        '''
        delete the emoji that is currently being 
        displayed on the main screen of the carousel
        '''
        if self.list.is_empty():#if the list is empty, the carousel is empty and there is no emoji
            print("The carousel is empty.")
            return
        current_node = self.list.get_current_node()
        self.list.remove_node(current_node)#remove the current node using the remove_node function
        self.display_carousel()  #display teh updated carousel
        

    def display_info(self):
        '''
        display the appropriate info of the emoji
        currently being displayed on the screen
        e.g the class the symbol and the name of the emoji
        '''
        if self.current_node:
            print(f"Object: {self.current_node.data['name']}")#name of the emoji
            print(f"Sym: {self.current_node.data['symbol']}")#the emoji
            emoji_class = self.get_emoji_class(self.current_node.data['name'])
            print(f"Class: {emoji_class}")#class emoji belongs too, i.e either food or animals
            input("Press any key to continue")
        else:
            print("The carousel is empty.")#if the carousel is empty, there is no info

    
    def get_emoji_class(self, emoji_name):
        '''
        gets the emoji class from the json file
        '''
        for category in self.emojis:
            if emoji_name in category['emojis']:
                return category['class']
        return None


    def display_carousel(self):
        '''
        This function displays the carousel, using a circular doubly linked list
        '''
        os.system('cls' if os.name == 'nt' else 'clear')  #clear the screen
        if self.list.is_empty():
            print("The carousel is empty.")  #display message when the carousel is empty
        else:
            empty_frame, one_item_frame, normal_frame = frames[1], frames[0], frames[0]#if carousel is not empty, get the index of empty carousel from the art.py, empty carousel is second item in art.py and more than 1 item in carousel is first item in art.py
            if self.list.size == 0:
                print(empty_frame)
                return
            elif self.list.size == 1:
                frame_to_use = one_item_frame
            else:
                frame_to_use = normal_frame
            
            current_node = self.current_node
            left_node = current_node.get_prev() if current_node.get_prev() != current_node else None#get the left node of the current node if current node exists
            right_node = current_node.get_next() if current_node.get_next() != current_node else None#get the right node of the current node if current node exists
    
            left_emoji = left_node.get_data()['symbol'] if left_node else '  '#left screen emoji
            center_emoji = current_node.get_data()['symbol']#main screen emoji
            right_emoji = right_node.get_data()['symbol'] if right_node else '  '#right screen emoji
    
            frame_with_emojis = frame_to_use.replace("()", center_emoji, 1)#replace the brackets with the emoji typed in by the user
            frame_with_emojis = frame_with_emojis.replace("()", right_emoji, 1)
            frame_with_emojis = frame_with_emojis.replace("()", left_emoji, 1)
    
            print(frame_with_emojis)#print the carousel


    def run(self):
        '''
        this function controls the entire implementation of the carousel
        '''
        go = True#variable to control while loop
        while go:
            if self.list.is_empty():#check whether the carousel is empty
                command = input("Enter ADD to add or Q to quit: ").upper()#prompt user to enter a command
                if command == 'ADD':#if user types add, add the emoji typed in by the user
                    self.add_node()
                elif command == 'Q':#if user types q, the carousel is exited
                    go = False
                else:
                    print("Invalid command. Please try again.")#if none of the 2 commans are types, user is reprompted to type a valid input
            else:
                self.display_carousel()#display carousel
                command = input("ADD: add a emoji frame\nDEL: delete current emoji frame\nINFO: retrieve info about current frame\nQ: Quit the program\n >>").upper()
                if command == 'ADD':
                    self.add_node()
                elif command == 'DEL':
                    self.delete_node()
                elif command == 'INFO':
                    self.display_info()
                elif command == 'LEFT':
                    print(frames[7])#animation for left arrow 
                    time.sleep(1)#delay of 1 second
                    self.list.move_left()#move carousel to the left
                    self.current_node = self.list.get_current_node()  
                elif command == 'RIGHT':
                    print(frames[4]) #animation for the right arrow 
                    time.sleep(1) #delay of 1 second
                    self.list.move_right()#move the carousel to the right
                    self.current_node = self.list.get_current_node() 
                elif command == 'Q':
                    go = False#exit the loop if user types in q
                else:
                    print("Invalid command. Please try again.")#if none of the commands shown are types in by the user, he is reprompted to enter a valid command

carousel = Carousel('emojis.json')#use the json file
carousel.run()
