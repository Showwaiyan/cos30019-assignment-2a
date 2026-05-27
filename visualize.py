import os
import sys
import math
import time
import heapq
from collections import deque
import pygame

# Import existing search services and registry
from search.services.parser import load_map
from search.registry import get_algorithm

# Initialize Pygame
pygame.init()
pygame.font.init()

# Define Color Palette (Modern Dark Theme with Neon Accents)
COLOR_BG = (11, 15, 25)          # Slate 950 (Main background)
COLOR_PANEL_BG = (17, 24, 39)    # Slate 900 (Panel background)
COLOR_SIDEBAR_BG = (15, 23, 42)  # Slate 900 (Sidebar background)
COLOR_BORDER = (31, 41, 55)      # Slate 800 (Panel border)
COLOR_BORDER_ACTIVE = (59, 130, 246) # Blue 500 (Active panel border)
COLOR_TEXT_PRIMARY = (243, 244, 246) # Gray 50 (Primary text)
COLOR_TEXT_MUTED = (156, 163, 175)   # Gray 400 (Muted text)

# Node colors
COLOR_NODE_UNEXPLORED = (71, 85, 105) # Slate 600
COLOR_NODE_START = (16, 185, 129)     # Emerald 500 (Green)
COLOR_NODE_GOAL = (244, 63, 94)       # Rose 500 (Red)
COLOR_NODE_VISITED = (245, 158, 11)   # Amber 500 (Orange)
COLOR_NODE_FRONTIER = (6, 182, 212)   # Cyan 500 (Cyan)
COLOR_NODE_CURRENT = (168, 85, 247)   # Purple 500 (Purple)

# Edge colors
COLOR_EDGE_UNEXPLORED = (51, 65, 85)  # Slate 700
COLOR_EDGE_EXPLORED = (14, 116, 144)  # Cyan 700 (Explored search tree edge)
COLOR_EDGE_PATH = (234, 179, 8)       # Yellow 500 (Glowing Path)

# Setup Fonts
def get_font(size, bold=False):
    # Fallback search for clean fonts
    font_names = ["helvetica", "arial", "segoeui", "sans-serif"]
    for name in font_names:
        try:
            return pygame.font.SysFont(name, size, bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

FONT_TITLE = get_font(20, bold=True)
FONT_SECTION = get_font(15, bold=True)
FONT_UI = get_font(14)
FONT_PANEL_HEADER = get_font(16, bold=True)
FONT_NODE = get_font(12, bold=True)
FONT_EDGE = get_font(10, bold=True)
FONT_METRICS = get_font(13)
FONT_METRICS_BOLD = get_font(13, bold=True)


# =====================================================================
# STEP-BY-STEP ALGORITHM GENERATORS (Matching existing search package)
# =====================================================================

def bfs_step(graph, origin, destinations):
    visited = set()
    queue = deque([(origin, [origin], 0)])
    nodes_created = 1
    came_from = {origin: None}

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    while queue:
        node_id, path, cost = queue.popleft()
        if node_id in visited:
            continue
        visited.add(node_id)

        yield {
            'current_node': node_id,
            'visited': set(visited),
            'frontier': {item[0] for item in queue},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if node_id in destinations:
            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': {item[0] for item in queue},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': path,
                'path_cost': cost
            }
            return

        node = graph.get(node_id)
        if node:
            waiting_nodes = {item[0] for item in queue}
            for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0]):
                if neighbor_id not in visited and neighbor_id not in waiting_nodes:
                    queue.append((neighbor_id, path + [neighbor_id], cost + edge_cost))
                    came_from[neighbor_id] = node_id
                    nodes_created += 1

            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': {item[0] for item in queue},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'searching'
            }

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': 0
    }


def dfs_step(graph, origin, destinations):
    visited = set()
    queue = deque([(origin, [origin], 0)])
    nodes_created = 1
    came_from = {origin: None}

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    while queue:
        node_id, path, cost = queue.pop() # LIFO Stack pop
        if node_id in visited:
            continue
        visited.add(node_id)

        yield {
            'current_node': node_id,
            'visited': set(visited),
            'frontier': {item[0] for item in queue},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if node_id in destinations:
            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': {item[0] for item in queue},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': path,
                'path_cost': cost
            }
            return

        node = graph.get(node_id)
        if node:
            waiting_nodes = {item[0] for item in queue}
            for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0], reverse=True):
                if neighbor_id not in visited:
                    queue.append((neighbor_id, path + [neighbor_id], cost + edge_cost))
                    came_from[neighbor_id] = node_id
                    if neighbor_id not in waiting_nodes:
                        nodes_created += 1

            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': {item[0] for item in queue},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'searching'
            }

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': 0
    }


def gbfs_step(graph, origin, destinations):
    if origin not in graph:
        yield {'status': 'failure', 'path': None, 'path_cost': 0, 'nodes_created': 0, 'visited': set(), 'frontier': set(), 'current_node': None, 'came_from': {}}
        return

    def get_heuristic(node_id):
        node = graph[node_id]
        return min(math.sqrt((node.x - graph[d].x) ** 2 + (node.y - graph[d].y) ** 2) for d in destinations)

    visited = set()
    open_set = []
    h_start = get_heuristic(origin)
    heapq.heappush(open_set, (h_start, origin))
    came_from = {}
    g_score = {origin: 0}
    nodes_created = 1

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue

        yield {
            'current_node': current,
            'visited': set(visited),
            'frontier': {item[1] for item in open_set},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if current in destinations:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(origin)
            path.reverse()

            yield {
                'current_node': current,
                'visited': set(visited) | {current},
                'frontier': {item[1] for item in open_set},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': path,
                'path_cost': g_score[current]
            }
            return

        visited.add(current)

        current_node = graph[current]
        for neighbor_id, edge_cost in current_node.neighbors:
            if neighbor_id in visited:
                continue
            if neighbor_id not in came_from:
                came_from[neighbor_id] = current
                g_score[neighbor_id] = g_score[current] + edge_cost
                h_val = get_heuristic(neighbor_id)
                heapq.heappush(open_set, (h_val, neighbor_id))
                nodes_created += 1

        yield {
            'current_node': current,
            'visited': set(visited),
            'frontier': {item[1] for item in open_set},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': 0
    }


def astar_step(graph, origin, destinations):
    if origin not in graph:
        yield {'status': 'failure', 'path': None, 'path_cost': 0, 'nodes_created': 0, 'visited': set(), 'frontier': set(), 'current_node': None, 'came_from': {}}
        return

    def get_heuristic(node_id):
        node = graph[node_id]
        return min(math.sqrt((node.x - graph[d].x) ** 2 + (node.y - graph[d].y) ** 2) for d in destinations)

    open_set = []
    counter = 0
    # open_set stores (f_score, neighbor_id, counter) matching actual astar.py implementation
    heapq.heappush(open_set, (0, origin, counter))
    came_from = {}
    g_score = {origin: 0}
    nodes_created = 1
    visited = set()

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    while open_set:
        _, current, _ = heapq.heappop(open_set)
        if current in visited:
            continue

        yield {
            'current_node': current,
            'visited': set(visited),
            'frontier': {item[1] for item in open_set},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if current in destinations:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(origin)
            path.reverse()

            yield {
                'current_node': current,
                'visited': set(visited) | {current},
                'frontier': {item[1] for item in open_set},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': path,
                'path_cost': g_score[current]
            }
            return

        visited.add(current)

        current_node = graph[current]
        for neighbor_id, edge_cost in current_node.neighbors:
            if neighbor_id in visited:
                continue

            tentative_g = g_score[current] + edge_cost
            if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                came_from[neighbor_id] = current
                g_score[neighbor_id] = tentative_g
                h_val = get_heuristic(neighbor_id)
                f_score = tentative_g + h_val
                counter += 1
                heapq.heappush(open_set, (f_score, neighbor_id, counter))
                nodes_created += 1

        yield {
            'current_node': current,
            'visited': set(visited),
            'frontier': {item[1] for item in open_set},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': 0
    }


def cus2_step(graph, origin, destinations):
    if origin not in graph:
        yield {'status': 'failure', 'path': None, 'path_cost': float('inf'), 'nodes_created': 0, 'visited': set(), 'frontier': set(), 'current_node': None, 'came_from': {}}
        return

    priorityQueue = [(0, origin, 0)]
    counter = 1
    visited_costs = {origin: 0}
    came_from = {origin: None}
    nodes_created = 1
    visited = set()

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    while priorityQueue:
        current_cost, current_node_id, _ = heapq.heappop(priorityQueue)
        if current_node_id in visited:
            continue

        yield {
            'current_node': current_node_id,
            'visited': set(visited),
            'frontier': {item[1] for item in priorityQueue},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if current_node_id in destinations:
            path = []
            node = current_node_id
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()

            yield {
                'current_node': current_node_id,
                'visited': set(visited) | {current_node_id},
                'frontier': {item[1] for item in priorityQueue},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': path,
                'path_cost': current_cost
            }
            return

        visited.add(current_node_id)

        current_node = graph[current_node_id]
        for neighbor_id, edge_cost in current_node.neighbors:
            new_cost = current_cost + edge_cost
            if neighbor_id not in visited_costs or new_cost < visited_costs[neighbor_id]:
                visited_costs[neighbor_id] = new_cost
                came_from[neighbor_id] = current_node_id
                nodes_created += 1
                heapq.heappush(priorityQueue, (new_cost, neighbor_id, counter))
                counter += 1

        yield {
            'current_node': current_node_id,
            'visited': set(visited),
            'frontier': {item[1] for item in priorityQueue},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

    yield {
        'current_node': None,
        'visited': set(visited),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': float('inf')
    }


# Map UI names to generator functions
GENERATORS = {
    "BFS": bfs_step,
    "DFS": dfs_step,
    "GBFS": gbfs_step,
    "A*": astar_step,
    "CUS2": cus2_step
}

# Registry Keys corresponding to the UI names
REGISTRY_KEYS = {
    "BFS": "BFS",
    "DFS": "DFS",
    "GBFS": "GBFS",
    "A*": "AS",
    "CUS2": "CUS2"
}


# =====================================================================
# UI WIDGET CLASSES
# =====================================================================

class Button:
    def __init__(self, x, y, w, h, text, bg_color, hover_color, text_color=COLOR_TEXT_PRIMARY, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=1, border_radius=6)
        
        txt_surf = FONT_UI.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)


class Checkbox:
    def __init__(self, x, y, label, checked=False, disabled=False, callback=None):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.callback = callback
        self.is_hovered = False

    def handle_event(self, event):
        if self.disabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos) or pygame.Rect(self.rect.x, self.rect.y, 200, 20).collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Allow clicking checkbox or label area
                click_rect = pygame.Rect(self.rect.x, self.rect.y, 200, 20)
                if click_rect.collidepoint(event.pos):
                    self.checked = not self.checked
                    if self.callback:
                        self.callback(self.checked)

    def draw(self, surface):
        # Draw box
        box_color = COLOR_PANEL_BG if not self.disabled else (30, 41, 59)
        border_color = COLOR_BORDER_ACTIVE if (self.checked and not self.disabled) else COLOR_BORDER
        if self.is_hovered and not self.disabled:
            border_color = (147, 197, 253) # Light blue

        pygame.draw.rect(surface, box_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=4)

        if self.checked:
            # Draw checkmark (an X inside)
            inner_rect = self.rect.inflate(-6, -6)
            pygame.draw.line(surface, COLOR_BORDER_ACTIVE if not self.disabled else COLOR_TEXT_MUTED, inner_rect.topleft, inner_rect.bottomright, 2)
            pygame.draw.line(surface, COLOR_BORDER_ACTIVE if not self.disabled else COLOR_TEXT_MUTED, inner_rect.bottomleft, inner_rect.topright, 2)

        # Draw label
        txt_color = COLOR_TEXT_PRIMARY if not self.disabled else COLOR_TEXT_MUTED
        txt_surf = FONT_UI.render(self.label, True, txt_color)
        surface.blit(txt_surf, (self.rect.right + 10, self.rect.y + 1))


class Slider:
    def __init__(self, x, y, w, min_val, max_val, current_val, label, callback=None):
        self.rect = pygame.Rect(x, y, w, 8)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.label = label
        self.callback = callback
        
        # Handle button
        self.handle_radius = 8
        self.dragging = False
        self.update_handle_x()

    def update_handle_x(self):
        val_range = self.max_val - self.min_val
        pct = (self.current_val - self.min_val) / val_range
        self.handle_x = self.rect.x + int(pct * self.rect.width)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                handle_rect = pygame.Rect(self.handle_x - self.handle_radius, self.rect.centery - self.handle_radius, self.handle_radius*2, self.handle_radius*2)
                if handle_rect.collidepoint(mouse_pos) or self.rect.inflate(0, 10).collidepoint(mouse_pos):
                    self.dragging = True
                    self.update_val_from_mouse(mouse_pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_val_from_mouse(event.pos[0])

    def update_val_from_mouse(self, mouse_x):
        pct = (mouse_x - self.rect.x) / self.rect.width
        pct = max(0.0, min(1.0, pct))
        val_range = self.max_val - self.min_val
        self.current_val = self.min_val + pct * val_range
        
        # Round logic if slider represents integers
        if isinstance(self.min_val, int) and isinstance(self.max_val, int):
            self.current_val = int(round(self.current_val))
            
        self.update_handle_x()
        if self.callback:
            self.callback(self.current_val)

    def draw(self, surface):
        # Draw label
        lbl_surf = FONT_UI.render(f"{self.label}: {self.current_val}", True, COLOR_TEXT_PRIMARY)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y - 20))

        # Draw track
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, border_radius=4)
        
        # Draw filled part
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_x - self.rect.x, self.rect.height)
        pygame.draw.rect(surface, COLOR_BORDER_ACTIVE, filled_rect, border_radius=4)

        # Draw handle
        pygame.draw.circle(surface, COLOR_TEXT_PRIMARY, (self.handle_x, self.rect.centery), self.handle_radius)
        pygame.draw.circle(surface, COLOR_BORDER_ACTIVE, (self.handle_x, self.rect.centery), self.handle_radius, width=2)


# =====================================================================
# DYNAMIC PANEL AND EDGE/NODE RENDERING HELPERS
# =====================================================================

def draw_directed_edge(surface, p1, p2, color, width=1, node_radius=15, arrow_size=10):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0:
        return

    ux = dx / dist
    uy = dy / dist

    # Back off the target point by the node's radius
    end_x = p2[0] - ux * node_radius
    end_y = p2[1] - uy * node_radius

    # Start at the edge of the source node
    start_x = p1[0] + ux * node_radius
    start_y = p1[1] + uy * node_radius

    # Draw the edge line
    pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)

    # Draw the arrowhead triangle
    base_x = end_x - ux * arrow_size
    base_y = end_y - uy * arrow_size

    perp_x = -uy * (arrow_size / 2)
    perp_y = ux * (arrow_size / 2)

    wing1 = (base_x + perp_x, base_y + perp_y)
    wing2 = (base_x - perp_x, base_y - perp_y)
    tip = (end_x, end_y)

    pygame.draw.polygon(surface, color, [tip, wing1, wing2])


def get_scaled_pos(node_x, node_y, min_x, max_x, min_y, max_y, panel_rect, padding=35):
    px, py, pw, ph = panel_rect
    
    # Calculate space available for graph (leave 40px at top for title, 100px at bottom for stats)
    draw_w = pw - 2 * padding
    draw_h = ph - 2 * padding - 140
    
    dx = max_x - min_x
    dy = max_y - min_y
    if dx == 0: dx = 1
    if dy == 0: dy = 1

    scale_x = draw_w / dx
    scale_y = draw_h / dy
    scale = min(scale_x, scale_y)

    # Center coordinates
    graph_w = dx * scale
    graph_h = dy * scale
    offset_x = px + padding + (draw_w - graph_w) / 2
    offset_y = py + padding + 40 + (draw_h - graph_h) / 2

    # Invert Y so larger Y values are higher up
    x_pos = offset_x + (node_x - min_x) * scale
    y_pos = offset_y + (max_y - node_y) * scale

    return int(x_pos), int(y_pos)


def compute_panel_rects(main_rect, k):
    mx, my, mw, mh = main_rect
    rects = []
    gap = 15

    if k == 1:
        rects.append((mx + gap, my + gap, mw - 2*gap, mh - 2*gap))
    elif k == 2:
        pw = (mw - 3*gap) // 2
        rects.append((mx + gap, my + gap, pw, mh - 2*gap))
        rects.append((mx + 2*gap + pw, my + gap, pw, mh - 2*gap))
    elif k <= 4:
        pw = (mw - 3*gap) // 2
        ph = (mh - 3*gap) // 2
        for r in range(2):
            for c in range(2):
                if len(rects) < k:
                    rects.append((
                        mx + gap + c*(pw + gap),
                        my + gap + r*(ph + gap),
                        pw,
                        ph
                    ))
    else:
        # 2x3 grid (up to 6 panels, we have max 5 active)
        pw = (mw - 4*gap) // 3
        ph = (mh - 3*gap) // 2
        for r in range(2):
            for c in range(3):
                if len(rects) < k:
                    rects.append((
                        mx + gap + c*(pw + gap),
                        my + gap + r*(ph + gap),
                        pw,
                        ph
                    ))
    return rects


# =====================================================================
# MAIN VISUALIZER APPLICATION CLASS
# =====================================================================

class VisualizerApp:
    def __init__(self):
        # Window configuration
        self.width = 1400
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Graph Search Visualizer — Side-by-Side Comparison")
        
        self.clock = pygame.time.Clock()
        self.running = True

        # Scan for map files in the 'maps/' directory
        self.maps_dir = "maps"
        self.map_files = []
        if os.path.exists(self.maps_dir):
            self.map_files = sorted([f for f in os.listdir(self.maps_dir) if f.endswith(".txt")])
        
        if not self.map_files:
            print("Error: No map text files found in the 'maps/' directory!")
            pygame.quit()
            sys.exit(1)

        self.current_map_idx = 0
        self.current_map_file = self.map_files[self.current_map_idx]

        # Algorithm Selection States
        # Order: BFS, DFS, GBFS, A*, CUS1 (disabled), CUS2
        self.algo_selections = {
            "BFS": True,
            "DFS": True,
            "GBFS": True,
            "A*": True,
            "CUS2": True
        }

        # Simulation States
        self.sim_running = False
        self.sim_speed = 5  # steps per second
        self.last_step_time = 0
        
        # Raw parsed map data
        self.origin = None
        self.destinations = []
        self.graph = {}
        self.min_x = 0
        self.max_x = 10
        self.min_y = 0
        self.max_y = 10

        # Simulation runner instances & latest states
        self.simulators = {}  # name -> generator
        self.sim_states = {}  # name -> latest state dict
        self.real_metrics = {} # name -> { 'path': list, 'cost': float, 'nodes_created': int, 'time_ms': float }

        # Setup GUI controls
        self.setup_ui()

        # Load the initial map
        self.load_map_file()

    def setup_ui(self):
        # UI Coordinates
        sidebar_x = 20
        y_offset = 30

        # Sidebar Title
        # Will render dynamically in draw()

        # 1. Map Navigation
        y_offset = 70
        self.btn_prev_map = Button(sidebar_x, y_offset, 45, 30, "<", COLOR_PANEL_BG, (30, 41, 59), callback=self.prev_map)
        self.btn_next_map = Button(sidebar_x + 235, y_offset, 45, 30, ">", COLOR_PANEL_BG, (30, 41, 59), callback=self.next_map)

        # 2. Algorithm Checkboxes
        y_offset = 150
        self.checkboxes = []
        
        # Selectable algorithms
        for name in ["BFS", "DFS", "GBFS", "A*", "CUS2"]:
            cb = Checkbox(sidebar_x, y_offset, name, checked=self.algo_selections[name], 
                          callback=lambda val, n=name: self.toggle_algo(n, val))
            self.checkboxes.append(cb)
            y_offset += 30

        # Add disabled CUS1
        cb_cus1 = Checkbox(sidebar_x, y_offset, "CUS1 (TBD / Not Implemented)", checked=False, disabled=True)
        self.checkboxes.append(cb_cus1)
        y_offset += 45

        # 3. Speed Slider
        self.speed_slider = Slider(sidebar_x, y_offset + 20, 280, 1, 60, self.sim_speed, "Speed (Steps/sec)", callback=self.set_speed)
        y_offset += 60

        # 4. Simulation Controls
        y_offset += 20
        self.btn_play_pause = Button(sidebar_x, y_offset, 135, 35, "Play", (16, 185, 129), (52, 211, 153), callback=self.toggle_play)
        self.btn_step = Button(sidebar_x + 145, y_offset, 135, 35, "Step", COLOR_PANEL_BG, (30, 41, 59), callback=self.step_once)
        y_offset += 45
        
        self.btn_reset = Button(sidebar_x, y_offset, 280, 35, "Reset Simulation", (239, 68, 68), (248, 113, 113), callback=self.reset_simulation)

    def load_map_file(self):
        filepath = os.path.join(self.maps_dir, self.current_map_file)
        try:
            self.origin, self.destinations, self.graph = load_map(filepath)
            
            # Find bounds for coordinate scaling
            xs = [node.x for node in self.graph.values()]
            ys = [node.y for node in self.graph.values()]
            
            self.min_x = min(xs) if xs else 0
            self.max_x = max(xs) if xs else 10
            self.min_y = min(ys) if ys else 0
            self.max_y = max(ys) if ys else 10
            
            # Add padding margin to bounds so nodes are never on the outer edge
            dx = self.max_x - self.min_x
            dy = self.max_y - self.min_y
            if dx == 0: dx = 1
            if dy == 0: dy = 1
            
            self.min_x -= dx * 0.05
            self.max_x += dx * 0.05
            self.min_y -= dy * 0.05
            self.max_y += dy * 0.05
            
            self.reset_simulation()
        except Exception as e:
            print(f"Error loading map file {self.current_map_file}: {e}")

    def prev_map(self):
        if self.map_files:
            self.current_map_idx = (self.current_map_idx - 1) % len(self.map_files)
            self.current_map_file = self.map_files[self.current_map_idx]
            self.load_map_file()

    def next_map(self):
        if self.map_files:
            self.current_map_idx = (self.current_map_idx + 1) % len(self.map_files)
            self.current_map_file = self.map_files[self.current_map_idx]
            self.load_map_file()

    def toggle_algo(self, name, checked):
        self.algo_selections[name] = checked
        self.reset_simulation()

    def set_speed(self, val):
        self.sim_speed = val

    def toggle_play(self):
        if self.sim_running:
            self.sim_running = False
            self.btn_play_pause.text = "Play"
            self.btn_play_pause.bg_color = (16, 185, 129)
            self.btn_play_pause.hover_color = (52, 211, 153)
        else:
            # If search is completed or failed, clicking play should restart it
            all_done = True
            for state in self.sim_states.values():
                if state['status'] == 'searching':
                    all_done = False
                    break
            
            if all_done and self.simulators:
                self.reset_simulation()
            
            self.sim_running = True
            self.btn_play_pause.text = "Pause"
            self.btn_play_pause.bg_color = (245, 158, 11) # Orange
            self.btn_play_pause.hover_color = (251, 191, 36)

    def reset_simulation(self):
        self.sim_running = False
        self.btn_play_pause.text = "Play"
        self.btn_play_pause.bg_color = (16, 185, 129)
        self.btn_play_pause.hover_color = (52, 211, 153)
        self.simulators.clear()
        self.sim_states.clear()
        self.real_metrics.clear()

        # Identify active algorithms
        active_algos = [name for name, sel in self.algo_selections.items() if sel]
        
        # 1. Run Synchronously to capture exact metrics
        for name in active_algos:
            reg_key = REGISTRY_KEYS[name]
            try:
                AlgoClass = get_algorithm(reg_key)
                
                # Measure CPU time precisely
                start = time.perf_counter()
                res = AlgoClass(self.graph).search(self.origin, self.destinations)
                elapsed = (time.perf_counter() - start) * 1000.0  # in ms
                
                self.real_metrics[name] = {
                    'path': res.path,
                    'cost': res.path_cost,
                    'nodes_created': res.nodes_created,
                    'time_ms': elapsed,
                    'destination': res.destination
                }
            except Exception as e:
                print(f"Error running algorithm {name} synchronously: {e}")
                self.real_metrics[name] = {
                    'path': None,
                    'cost': 0.0,
                    'nodes_created': 0,
                    'time_ms': 0.0,
                    'destination': None
                }

        # 2. Instantiate step generators
        for name in active_algos:
            gen_func = GENERATORS[name]
            self.simulators[name] = gen_func(self.graph, self.origin, self.destinations)
            
            # Get the initial setup state from generator
            try:
                self.sim_states[name] = next(self.simulators[name])
            except StopIteration:
                pass

    def step_once(self):
        # Advance each simulator by one step
        any_advancements = False
        for name, simulator in list(self.simulators.items()):
            current_state = self.sim_states.get(name)
            if current_state and current_state['status'] == 'searching':
                try:
                    self.sim_states[name] = next(simulator)
                    any_advancements = True
                except StopIteration:
                    pass
        
        # If we cannot advance further, pause play
        if not any_advancements and self.sim_running:
            self.toggle_play()

    def tick(self):
        if not self.sim_running:
            return
        
        now = time.time()
        delay = 1.0 / self.sim_speed
        if now - self.last_step_time >= delay:
            self.step_once()
            self.last_step_time = now

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Feed events to UI controls
            self.btn_prev_map.handle_event(event)
            self.btn_next_map.handle_event(event)
            for cb in self.checkboxes:
                cb.handle_event(event)
            self.speed_slider.handle_event(event)
            self.btn_play_pause.handle_event(event)
            self.btn_step.handle_event(event)
            self.btn_reset.handle_event(event)

    def draw(self):
        # 1. Clear Screen
        self.screen.fill(COLOR_BG)

        # =====================================================================
        # SIDEBAR DRAWING
        # =====================================================================
        sidebar_rect = pygame.Rect(0, 0, 320, self.height)
        pygame.draw.rect(self.screen, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(self.screen, COLOR_BORDER, (320, 0), (320, self.height), 2)

        # Header Text
        title_surf = FONT_TITLE.render("ROUTE FINDING SEARCH", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(title_surf, (20, 20))
        subtitle_surf = FONT_SECTION.render("Algorithm Visualizer", True, COLOR_BORDER_ACTIVE)
        self.screen.blit(subtitle_surf, (20, 42))

        # Map Selector Panel
        lbl_map = FONT_SECTION.render("SELECT MAP GRAPH", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_map, (20, 105))
        
        self.btn_prev_map.draw(self.screen)
        map_name_surf = FONT_UI.render(self.current_map_file, True, COLOR_TEXT_PRIMARY)
        map_name_rect = map_name_surf.get_rect(center=(160, 85))
        self.screen.blit(map_name_surf, map_name_rect)
        self.btn_next_map.draw(self.screen)

        # Draw Checkboxes
        lbl_algos = FONT_SECTION.render("SEARCH ALGORITHMS", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_algos, (20, 130))
        for cb in self.checkboxes:
            cb.draw(self.screen)

        # Speed Slider & Controls
        self.speed_slider.draw(self.screen)
        self.btn_play_pause.draw(self.screen)
        self.btn_step.draw(self.screen)
        self.btn_reset.draw(self.screen)

        # Legend panel at bottom of sidebar
        legend_y = 660
        lbl_legend = FONT_SECTION.render("LEGEND", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_legend, (20, legend_y))
        
        legend_items = [
            ("Start Node", COLOR_NODE_START),
            ("Goal Node", COLOR_NODE_GOAL),
            ("Current Node", COLOR_NODE_CURRENT),
            ("Frontier Node", COLOR_NODE_FRONTIER),
            ("Explored Node", COLOR_NODE_VISITED),
            ("Unexplored Edge", COLOR_EDGE_UNEXPLORED),
            ("Final Path Edge", COLOR_EDGE_PATH)
        ]
        
        item_y = legend_y + 25
        for text, color in legend_items:
            # Draw color sample (circle for nodes, line for edges)
            if "Edge" in text:
                pygame.draw.line(self.screen, color, (25, item_y + 7), (40, item_y + 7), 3)
            else:
                pygame.draw.circle(self.screen, color, (32, item_y + 7), 6)
                
            txt_surf = FONT_UI.render(text, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(txt_surf, (55, item_y))
            item_y += 22

        # =====================================================================
        # MAIN GRID DRAWING
        # =====================================================================
        main_rect = (320, 0, 1080, 900)
        active_algos = [name for name, sel in self.algo_selections.items() if sel]
        k = len(active_algos)

        if k == 0:
            # Show empty placeholder message
            msg_surf = FONT_TITLE.render("Please select at least one algorithm to visualize.", True, COLOR_TEXT_MUTED)
            msg_rect = msg_surf.get_rect(center=(860, 450))
            self.screen.blit(msg_surf, msg_rect)
            return

        panel_rects = compute_panel_rects(main_rect, k)

        for i, name in enumerate(active_algos):
            rect = panel_rects[i]
            px, py, pw, ph = rect

            # Draw panel background & border
            state = self.sim_states.get(name, {})
            status = state.get('status', 'searching')
            
            border_col = COLOR_BORDER
            if status == 'searching' and state.get('current_node') is not None:
                border_col = COLOR_BORDER_ACTIVE
            elif status == 'success':
                border_col = COLOR_NODE_START
            elif status == 'failure':
                border_col = COLOR_NODE_GOAL

            pygame.draw.rect(self.screen, COLOR_PANEL_BG, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_col, rect, width=2, border_radius=8)

            # Panel Title
            title_text = f"{name}"
            if name == "CUS2":
                title_text += " (Dijkstra)"
            title_surf = FONT_PANEL_HEADER.render(title_text, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(title_surf, (px + 15, py + 12))

            # Retrieve state data
            visited_set = state.get('visited', set())
            frontier_set = state.get('frontier', set())
            current_node_id = state.get('current_node', None)
            came_from = state.get('came_from', {})
            path = state.get('path', None)

            # Render Graph within this panel
            if self.graph:
                # First pass: Draw edges
                for node_id, node in self.graph.items():
                    p1 = get_scaled_pos(node.x, node.y, self.min_x, self.max_x, self.min_y, self.max_y, rect)
                    
                    for neighbor_id, cost in node.neighbors:
                        p2 = get_scaled_pos(self.graph[neighbor_id].x, self.graph[neighbor_id].y, self.min_x, self.max_x, self.min_y, self.max_y, rect)
                        
                        # Decide edge color and width
                        edge_color = COLOR_EDGE_UNEXPLORED
                        edge_width = 1
                        
                        # Check if it's part of the final path
                        is_path_edge = False
                        if path and node_id in path and neighbor_id in path:
                            # Verify ordering in path list
                            idx1 = path.index(node_id)
                            idx2 = path.index(neighbor_id)
                            if idx2 == idx1 + 1:
                                is_path_edge = True

                        if is_path_edge:
                            edge_color = COLOR_EDGE_PATH
                            edge_width = 3
                        elif came_from.get(neighbor_id) == node_id:
                            # It's an explored edge of the search tree
                            edge_color = COLOR_EDGE_EXPLORED
                            edge_width = 2

                        draw_directed_edge(self.screen, p1, p2, edge_color, width=edge_width, node_radius=14, arrow_size=8)
                        
                        # Draw Edge Weight Label (offset slightly perpendicular to line)
                        # Placement at 65% distance from start to end (to avoid overlapping bidirectional text)
                        lbl_x = p1[0] + 0.60 * (p2[0] - p1[0])
                        lbl_y = p1[1] + 0.60 * (p2[1] - p1[1])
                        
                        # Compute normal vector for offset
                        dx = p2[0] - p1[0]
                        dy = p2[1] - p1[1]
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist > 0:
                            nx = -dy / dist
                            ny = dx / dist
                            lbl_x += nx * 10
                            lbl_y += ny * 10
                        
                        # Draw small backdrop box for label readability
                        weight_surf = FONT_EDGE.render(str(cost), True, COLOR_TEXT_MUTED)
                        bg_rect = weight_surf.get_rect(center=(lbl_x, lbl_y))
                        pygame.draw.rect(self.screen, COLOR_BG, bg_rect.inflate(4, 2))
                        self.screen.blit(weight_surf, bg_rect)

                # Second pass: Draw Nodes
                for node_id, node in self.graph.items():
                    pos = get_scaled_pos(node.x, node.y, self.min_x, self.max_x, self.min_y, self.max_y, rect)
                    
                    # Decide node color based on status
                    node_color = COLOR_NODE_UNEXPLORED
                    if node_id == self.origin:
                        node_color = COLOR_NODE_START
                    elif node_id in self.destinations:
                        node_color = COLOR_NODE_GOAL
                    elif path and node_id in path:
                        node_color = COLOR_NODE_START if node_id == self.origin else (COLOR_NODE_GOAL if node_id in self.destinations else COLOR_EDGE_PATH)
                    elif node_id == current_node_id:
                        node_color = COLOR_NODE_CURRENT
                    elif node_id in frontier_set:
                        node_color = COLOR_NODE_FRONTIER
                    elif node_id in visited_set:
                        node_color = COLOR_NODE_VISITED

                    # Glow effect for active/path nodes
                    if node_color in [COLOR_NODE_START, COLOR_NODE_GOAL, COLOR_EDGE_PATH, COLOR_NODE_CURRENT]:
                        pygame.draw.circle(self.screen, node_color, pos, 16, width=2)

                    pygame.draw.circle(self.screen, node_color, pos, 13)
                    pygame.draw.circle(self.screen, COLOR_TEXT_PRIMARY, pos, 13, width=1)
                    
                    # Draw node number inside
                    num_surf = FONT_NODE.render(str(node_id), True, COLOR_TEXT_PRIMARY)
                    num_rect = num_surf.get_rect(center=pos)
                    self.screen.blit(num_surf, num_rect)

            # =================================================================
            # STATS & METRICS DISPLAY OVERLAY
            # =================================================================
            metrics_box = pygame.Rect(px + 10, py + ph - 130, pw - 20, 120)
            pygame.draw.rect(self.screen, COLOR_BG, metrics_box, border_radius=6)
            pygame.draw.rect(self.screen, COLOR_BORDER, metrics_box, width=1, border_radius=6)

            metrics = self.real_metrics.get(name, {})
            official_cost = metrics.get('cost', float('inf'))
            official_created = metrics.get('nodes_created', 0)
            official_time = metrics.get('time_ms', 0.0)
            official_path = metrics.get('path', None)

            # Format status text
            status_text = "SEARCHING..."
            status_color = COLOR_NODE_FRONTIER
            if status == 'success':
                status_text = "GOAL REACHED"
                status_color = COLOR_NODE_START
            elif status == 'failure':
                status_text = "NO PATH FOUND"
                status_color = COLOR_NODE_GOAL

            stat_lbl_surf = FONT_METRICS.render("Status: ", True, COLOR_TEXT_MUTED)
            stat_val_surf = FONT_METRICS_BOLD.render(status_text, True, status_color)
            self.screen.blit(stat_lbl_surf, (px + 20, py + ph - 120))
            self.screen.blit(stat_val_surf, (px + 70, py + ph - 120))

            # Nodes Created (Live and Official)
            live_created = state.get('nodes_created', 0)
            node_str = f"Nodes Created: {live_created} (Official: {official_created})"
            node_surf = FONT_METRICS.render(node_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(node_surf, (px + 20, py + ph - 100))

            # Path cost
            cost_str = f"Path Cost: {official_cost if official_path else 'N/A'}"
            if official_cost == float('inf'):
                cost_str = "Path Cost: N/A (No solution)"
            cost_surf = FONT_METRICS.render(cost_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(cost_surf, (px + 20, py + ph - 80))

            # Execution time
            time_str = f"CPU Exec Time: {official_time:.4f} ms"
            time_surf = FONT_METRICS.render(time_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(time_surf, (px + 20, py + ph - 60))

            # Path list display
            if status == 'success' and path:
                path_str = "Path: " + " -> ".join(map(str, path))
            else:
                path_str = "Path: Searching..."
                if status == 'failure':
                    path_str = "Path: None"
            
            # Wrap path text if too long
            max_pixels = pw - 40
            if FONT_METRICS.size(path_str)[0] > max_pixels:
                # Truncate and add ellipsis
                while FONT_METRICS.size(path_str + "...")[0] > max_pixels and len(path_str) > 10:
                    path_str = path_str[:-1]
                path_str += "..."
                
            path_surf = FONT_METRICS.render(path_str, True, COLOR_EDGE_PATH if status == 'success' else COLOR_TEXT_MUTED)
            self.screen.blit(path_surf, (px + 20, py + ph - 40))

        # Draw a tiny info footer on the main screen
        footer_surf = FONT_METRICS.render("Visualizer advances frame-by-frame dynamically. Start node has glowing outer ring.", True, COLOR_TEXT_MUTED)
        self.screen.blit(footer_surf, (340, self.height - 25))

    def run(self):
        while self.running:
            self.handle_events()
            self.tick()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = VisualizerApp()
    app.run()
