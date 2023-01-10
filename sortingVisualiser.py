import pygame
import random
# import math
pygame.init()

class DrawInformation:
    # kinda global values 
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    # BACKGROUND_COLOR = '#27282c'
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]
    LR_PADDING = 100
    TOP_PADDING = 150

    FONT = pygame.font.SysFont('arial', 30)
    LARGER_FONT = pygame.font.SysFont('arial', 40)


    def __init__(self, width, height, arr):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algo Visualizer")
        self.set_arr(arr)

    # set dynamic width and height of each bar depending upon range of arr
    def set_arr(self, arr):
        self.arr = arr
        self.min_val = min(arr)
        self.max_val = max(arr)
        # drawable width is equally divided to each element
        # (total width of screen - 100px) / numOfElements
        self.dynamic_width = int((self.width - self.LR_PADDING) / len(arr))
        # dynamic_height is the height of a single pixel depending upon max and min element of arr. So, the height of a elem will scale like (currElem * dynamic_height)
        self.dynamic_height = int((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.LR_PADDING // 2  # start from bottom-left after padding

# Fills the whole canvas with a solid background color


def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)  # draw it
    # showing control shortcuts
    shortcuts = draw_info.FONT.render("S:Sort   R:Reset   A:Ascending   D:Descending", 1, draw_info.BLACK)
    # center aligning text
    draw_info.window.blit(shortcuts, ((draw_info.width - shortcuts.get_width()) / 2, 5))
    #showing sort types
    sorting_type = draw_info.FONT.render("B:Bubble Sort   Q:Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting_type, ((draw_info.width - sorting_type.get_width()) / 2, 40))

    draw_list(draw_info)
    pygame.display.update()  # update to actually see it

# drawing the list/arr
# draw each elem/block with their gradient colors, set x and y coordinate for each block


def draw_list(draw_info, color_positions={}, clear_bg = False):  # {index : color}
    arr = draw_info.arr
    if clear_bg:
        #capturing the section of window where the list is present in order to clr/update it
        clear_section = (draw_info.LR_PADDING // 2, draw_info.TOP_PADDING, draw_info.width - draw_info.LR_PADDING, draw_info.height - draw_info.TOP_PADDING)
        #draw rectangle in pygame(where, color, x, y, length, breadth)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_section)

    for i, val in enumerate(arr):
        x = draw_info.start_x + i * draw_info.dynamic_width
        # y = val * draw_info.dynamic_height      (NOT THAT SIMPLE BC DRAWING STARTS FROM TOP LEFT CORNER (0,0)) INSTEAD:
        # subtracting min_val gives us how much larger we are from minimum(takes care of negative values)
        y = draw_info.height - (val - draw_info.min_val) * draw_info.dynamic_height

        # color resets after every three elements (0, 1, 2)
        color = draw_info.GRADIENTS[i % 3]
        
        if i in color_positions:
            color = color_positions[i] # override color
            #draw rectangle in pygame(where, color, x, y, length, breadth)
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.dynamic_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# Generate arr of random nums between min and max values
def generate_starting_arr(n, min_val, max_val):
    arr = []
    for _ in range(min_val, max_val):
        random_val = random.randint(min_val, max_val)
        arr.append(random_val)

    return arr

# Bubble Sort Implementation

def bubble_sort(draw_info, ascending=True):
    arr = draw_info.arr

    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            num1 = arr[j]
            num2 = arr[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True  # allows reset in middle of sorting
        # draw_list(draw_info, {(len(arr)- 1): draw_info.GREEN}, True)
    return arr


# def quick_sort(draw_info, ascending=True):
    

# Creating window and event loop
def main():
    run = True
    clock = pygame.time.Clock()
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None
    

    n = 50
    min_val = 0
    max_val = 100
    arr = generate_starting_arr(n, min_val, max_val)
    
    draw_info = DrawInformation(800, 600, arr)
    while run:
        clock.tick(1400)  # update 60 frames per second

        if sorting:
            try:
                next(sorting_algo_generator)    
            except StopIteration:
                sorting = False
        else:            
            draw(draw_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # resetting arr with R key
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                arr = generate_starting_arr(n, min_val, max_val)
                draw_info.set_arr(arr)
                sorting = False

            elif event.key == pygame.K_s and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

    pygame.quit()  # quit when cross button is clicked


# run main only from here
if __name__ == "__main__":
    main()
