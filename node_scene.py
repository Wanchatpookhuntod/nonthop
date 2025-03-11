import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Window")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
fullscreen = False
nodes = [pygame.Rect(10, 10, 100, 50)]
edges = []
dragging = False
dragging_node = None
drawing_edge = False
start_pos = None
current_node = None
input_node = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for node_rect in nodes:
                    output_circle_pos = (node_rect.right, node_rect.centery)
                    input_circle_pos = (node_rect.left, node_rect.centery)
                    if pygame.Rect(output_circle_pos[0] - 5, output_circle_pos[1] - 5, 10, 10).collidepoint(event.pos):
                        drawing_edge = True
                        start_pos = output_circle_pos
                        current_node = node_rect
                        break
                    elif pygame.Rect(input_circle_pos[0] - 5, input_circle_pos[1] - 5, 10, 10).collidepoint(event.pos):
                        input_node = node_rect
                        break
                    elif node_rect.collidepoint(event.pos):
                        dragging = True
                        dragging_node = node_rect
                        mouse_x, mouse_y = event.pos
                        offset_x = node_rect.x - mouse_x
                        offset_y = node_rect.y - mouse_y
                        break
            elif event.button == 3:  # Right mouse button
                new_node = pygame.Rect(event.pos[0], event.pos[1], 100, 50)
                nodes.append(new_node)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if drawing_edge:
                    drawing_edge = False
                    for node_rect in nodes:
                        input_circle_pos = (node_rect.left, node_rect.centery)
                        if pygame.Rect(input_circle_pos[0] - 5, input_circle_pos[1] - 5, 10, 10).collidepoint(event.pos):
                            edges.append((current_node, node_rect))
                            break
                    start_pos = None
                    current_node = None
                dragging = False
                dragging_node = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and dragging_node:
                mouse_x, mouse_y = event.pos
                dragging_node.x = mouse_x + offset_x
                dragging_node.y = mouse_y + offset_y

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))

    # Draw all edges
    for edge in edges:
        start_node, end_node = edge
        start_pos = (start_node.right, start_node.centery)
        end_pos = (end_node.left, end_node.centery)
        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)

    # Draw all nodes
    for node_rect in nodes:
        pygame.draw.rect(screen, (255, 0, 0), node_rect)
        # Draw a small circle at the right center of each node (output)
        output_circle_pos = (node_rect.right, node_rect.centery)
        pygame.draw.circle(screen, (0, 255, 0), output_circle_pos, 5)
        # Draw a small circle at the left center of each node (input)
        input_circle_pos = (node_rect.left, node_rect.centery)
        pygame.draw.circle(screen, (0, 0, 255), input_circle_pos, 5)

    # Update start_pos if drawing_edge is True
    if drawing_edge and current_node:
        start_pos = (current_node.right, current_node.centery)

    # Draw the edge being drawn
    if drawing_edge and start_pos:
        # Check if the mouse is over an input circle
        for node_rect in nodes:
            input_circle_pos = (node_rect.left, node_rect.centery)
            if pygame.Rect(input_circle_pos[0] - 5, input_circle_pos[1] - 5, 10, 10).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.line(screen, (255, 255, 255), start_pos, input_circle_pos, 2)
                break

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()