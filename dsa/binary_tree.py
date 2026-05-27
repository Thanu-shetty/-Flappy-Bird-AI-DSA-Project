import pygame
import random
from utils.constants import *

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class BinaryTreeChallenge:
    def __init__(self, screen):
        self.screen = screen
        self.tree = None
        self.values = []
        self.current_step = 0
        self.problem = None
        self.user_input = ""
        self.message = ""
        self.score = 0
        self.completed = False
        self.generate_problem()
        
    def generate_problem(self):
        problem_types = [
            "insert", "traverse", "search", "find_min", "find_max"
        ]
        self.problem_type = random.choice(problem_types)
        
        # Generate random values
        self.values = random.sample(range(1, 100), 7)
        self.tree = self.build_tree(self.values.copy())
        
        if self.problem_type == "insert":
            new_value = random.randint(1, 100)
            while new_value in self.values:
                new_value = random.randint(1, 100)
            self.problem = f"Insert value {new_value} into the BST"
            self.correct_answer = sorted(self.values + [new_value])
            
        elif self.problem_type == "traverse":
            traverse_types = ["inorder", "preorder", "postorder"]
            self.traverse_type = random.choice(traverse_types)
            self.problem = f"Perform {self.traverse_type} traversal"
            self.correct_answer = self.get_traversal(self.traverse_type)
            
        elif self.problem_type == "search":
            target = random.choice(self.values)
            self.problem = f"Search for value {target} in the BST"
            self.correct_answer = "Found"
            
        elif self.problem_type == "find_min":
            self.problem = "Find the minimum value in the BST"
            self.correct_answer = str(min(self.values))
            
        elif self.problem_type == "find_max":
            self.problem = "Find the maximum value in the BST"
            self.correct_answer = str(max(self.values))
    
    def build_tree(self, values):
        if not values:
            return None
            
        root = TreeNode(values[0])
        for value in values[1:]:
            self.insert_node(root, value)
        return root
    
    def insert_node(self, root, value):
        if value < root.value:
            if root.left is None:
                root.left = TreeNode(value)
            else:
                self.insert_node(root.left, value)
        else:
            if root.right is None:
                root.right = TreeNode(value)
            else:
                self.insert_node(root.right, value)
    
    def get_traversal(self, order_type):
        result = []
        if order_type == "inorder":
            self.inorder_traversal(self.tree, result)
        elif order_type == "preorder":
            self.preorder_traversal(self.tree, result)
        elif order_type == "postorder":
            self.postorder_traversal(self.tree, result)
        return ' '.join(map(str, result))
    
    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.value)
            self.inorder_traversal(node.right, result)
    
    def preorder_traversal(self, node, result):
        if node:
            result.append(node.value)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)
    
    def postorder_traversal(self, node, result):
        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.value)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode
    
    def check_answer(self):
        if self.problem_type in ["find_min", "find_max", "search"]:
            user_answer = self.user_input.strip()
        else:
            user_answer = [int(x) for x in self.user_input.split() if x.isdigit()]
            
        if str(user_answer) == str(self.correct_answer):
            self.message = "Correct! +10 points"
            self.score = 10
            self.completed = True
        else:
            self.message = f"Wrong! Correct answer: {self.correct_answer}"
            self.score = 0
            self.completed = True
    
    def update(self):
        pass
    
    def draw(self):
        # Draw challenge background
        challenge_rect = pygame.Rect(100, 100, 800, 500)
        pygame.draw.rect(self.screen, (50, 50, 80), challenge_rect)
        pygame.draw.rect(self.screen, WHITE, challenge_rect, 2)
        
        # Draw problem
        font = pygame.font.SysFont('Arial', 24)
        problem_text = font.render(self.problem, True, WHITE)
        self.screen.blit(problem_text, (120, 120))
        
        # Draw input box
        input_rect = pygame.Rect(120, 180, 400, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        input_text = font.render(self.user_input, True, WHITE)
        self.screen.blit(input_text, (130, 185))
        
        # Draw message
        if self.message:
            message_text = font.render(self.message, True, YELLOW)
            self.screen.blit(message_text, (120, 240))
        
        # Draw tree visualization
        self.draw_tree(400, 300, self.tree)
    
    def draw_tree(self, x, y, node, level=1, offset=150):
        if not node:
            return
            
        node.x = x
        node.y = y
        
        # Draw node
        pygame.draw.circle(self.screen, GREEN, (x, y), 20)
        pygame.draw.circle(self.screen, BLACK, (x, y), 20, 2)
        
        value_text = pygame.font.SysFont('Arial', 18).render(str(node.value), True, BLACK)
        self.screen.blit(value_text, (x - 8, y - 8))
        
        # Draw left child
        if node.left:
            left_x = x - offset
            left_y = y + 80
            pygame.draw.line(self.screen, WHITE, (x, y + 20), (left_x, left_y - 20), 2)
            self.draw_tree(left_x, left_y, node.left, level + 1, offset // 1.5)
        
        # Draw right child
        if node.right:
            right_x = x + offset
            right_y = y + 80
            pygame.draw.line(self.screen, WHITE, (x, y + 20), (right_x, right_y - 20), 2)
            self.draw_tree(right_x, right_y, node.right, level + 1, offset // 1.5)
    
    def is_completed(self):
        return self.completed
    
    def get_score(self):
        return self.score