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

FONT_TITLE = None
FONT_SECTION = None
FONT_UI = None
FONT_PANEL_HEADER = None
FONT_NODE = None
FONT_EDGE = None
FONT_METRICS = None
FONT_METRICS_BOLD = None

def update_fonts(scale):
    global FONT_TITLE, FONT_SECTION, FONT_UI, FONT_PANEL_HEADER, FONT_NODE, FONT_EDGE, FONT_METRICS, FONT_METRICS_BOLD
    
    # UI / Sidebar scale is capped or scaled down to prevent overflowing the 320px sidebar
    ui_scale = 1.0 + (scale - 1.0) * 0.3
    ui_scale = max(0.9, min(ui_scale, 1.3))
    
    # Main panel scale scales more dynamically
    main_scale = scale
    
    FONT_TITLE = get_font(max(16, int(20 * ui_scale)), bold=True)
    FONT_SECTION = get_font(max(12, int(15 * ui_scale)), bold=True)
    FONT_UI = get_font(max(11, int(14 * ui_scale)))
    
    FONT_PANEL_HEADER = get_font(max(13, int(16 * main_scale)), bold=True)
    FONT_NODE = get_font(max(9, int(12 * main_scale)), bold=True)
    FONT_EDGE = get_font(max(8, int(10 * main_scale)), bold=True)
    FONT_METRICS = get_font(max(10, int(13 * main_scale)))
    FONT_METRICS_BOLD = get_font(max(10, int(13 * main_scale)), bold=True)

# Run initial load at default scale of 1.0
update_fonts(1.0)


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


def cus1_step(graph, origin, destinations):
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


def cus2_step(graph, origin, destinations):
    if origin not in graph:
        yield {
            'status': 'failure',
            'path': None,
            'path_cost': 0,
            'nodes_created': 0,
            'visited': set(),
            'frontier': set(),
            'current_node': None,
            'came_from': {}
        }
        return

    def get_heuristic(node_id):
        node = graph[node_id]
        return min(math.sqrt((node.x - graph[d].x) ** 2 + (node.y - graph[d].y) ** 2) for d in destinations)

    threshold = get_heuristic(origin)
    nodes_created = 1
    seen_nodes = {origin}
    came_from = {origin: None}

    yield {
        'current_node': None,
        'visited': set(),
        'frontier': {origin},
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'searching'
    }

    # Recursive generator helper
    def dfs_generator(node_id, g, path, visited):
        nonlocal nodes_created
        f = g + get_heuristic(node_id)

        if f > threshold:
            if f < next_threshold[0]:
                next_threshold[0] = f
            return None

        # Yield when starting to explore this node
        yield {
            'current_node': node_id,
            'visited': set(visited),
            'frontier': set(seen_nodes) - set(visited) - {node_id},
            'came_from': dict(came_from),
            'nodes_created': nodes_created,
            'status': 'searching'
        }

        if node_id in destinations:
            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': set(seen_nodes) - set(visited) - {node_id},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'success',
                'path': list(path),
                'path_cost': g
            }
            return (list(path), g)

        node = graph[node_id]
        sorted_neighbors = sorted(
            node.neighbors, key=lambda x: (g + x[1] + get_heuristic(x[0]), x[0])
        )

        for neighbor_id, edge_cost in sorted_neighbors:
            if neighbor_id in visited:
                continue

            if neighbor_id not in seen_nodes:
                seen_nodes.add(neighbor_id)
                nodes_created += 1

            came_from[neighbor_id] = node_id
            visited.add(neighbor_id)
            path.append(neighbor_id)

            result = yield from dfs_generator(neighbor_id, g + edge_cost, path, visited)
            if result is not None:
                return result

            # Backtrack
            path.pop()
            visited.remove(neighbor_id)

            # Yield after backtracking
            yield {
                'current_node': node_id,
                'visited': set(visited),
                'frontier': set(seen_nodes) - set(visited) - {node_id},
                'came_from': dict(came_from),
                'nodes_created': nodes_created,
                'status': 'searching'
            }

        return None

    while True:
        next_threshold = [float("inf")]
        # Reset came_from pointers to avoid showing stale paths from previous iterations
        came_from = {origin: None}
        
        result = yield from dfs_generator(origin, 0, [origin], {origin})
        if result is not None:
            return

        if next_threshold[0] == float("inf"):
            break
        threshold = next_threshold[0]

    yield {
        'current_node': None,
        'visited': set(seen_nodes),
        'frontier': set(),
        'came_from': dict(came_from),
        'nodes_created': nodes_created,
        'status': 'failure',
        'path': None,
        'path_cost': 0
    }


# Map UI names to generator functions
GENERATORS = {
    "BFS": bfs_step,
    "DFS": dfs_step,
    "GBFS": gbfs_step,
    "A*": astar_step,
    "CUS1": cus1_step,
    "CUS2": cus2_step
}

# Registry Keys corresponding to the UI names
REGISTRY_KEYS = {
    "BFS": "BFS",
    "DFS": "DFS",
    "GBFS": "GBFS",
    "A*": "AS",
    "CUS1": "CUS1",
    "CUS2": "CUS2"
}


# =====================================================================
# UI WIDGET CLASSES
# =====================================================================

class Button:
    def __init__(self, x, y, w, h, text, bg_color, hover_color, text_color=COLOR_TEXT_PRIMARY, callback=None, disabled=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.is_hovered = False
        self.disabled = disabled

    def handle_event(self, event):
        if self.disabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()

    def draw(self, surface):
        if self.disabled:
            color = COLOR_PANEL_BG
            text_color = COLOR_TEXT_MUTED
        else:
            color = self.hover_color if self.is_hovered else self.bg_color
            text_color = self.text_color
            
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=1, border_radius=6)
        
        txt_surf = FONT_UI.render(self.text, True, text_color)
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


class TextInput:
    def __init__(self, x, y, w, h, placeholder="", callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.callback = callback
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.callback:
                    self.callback(self.text)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add printable characters
                if event.unicode and event.unicode.isprintable():
                    self.text += event.unicode

    def update(self):
        # Blink cursor
        self.cursor_timer += 1
        if self.cursor_timer >= 30: # roughly every 500ms at 60 FPS
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        box_color = COLOR_PANEL_BG
        border_color = COLOR_BORDER_ACTIVE if self.active else (COLOR_BORDER if not self.is_hovered else (147, 197, 253))
        
        pygame.draw.rect(surface, box_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, width=2 if self.active else 1, border_radius=6)

        # Draw text or placeholder
        if self.text:
            disp_text = self.text
            txt_color = COLOR_TEXT_PRIMARY
        else:
            disp_text = self.placeholder
            txt_color = COLOR_TEXT_MUTED

        txt_surf = FONT_UI.render(disp_text, True, txt_color)
        text_w, text_h = FONT_UI.size(disp_text)
        
        max_w = self.rect.width - 16
        if text_w > max_w:
            # Scroll text left so the end of text is always visible
            start_idx = 0
            while FONT_UI.size(disp_text[start_idx:])[0] > max_w:
                start_idx += 1
            disp_surf = FONT_UI.render(disp_text[start_idx:], True, txt_color)
            visible_w = FONT_UI.size(disp_text[start_idx:])[0]
        else:
            disp_surf = txt_surf
            visible_w = text_w

        surface.blit(disp_surf, (self.rect.x + 8, self.rect.y + (self.rect.height - disp_surf.get_height()) // 2))

        # Blinking cursor line
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 8 + visible_w + 2
            cursor_y1 = self.rect.y + 6
            cursor_y2 = self.rect.y + self.rect.height - 6
            pygame.draw.line(surface, COLOR_TEXT_PRIMARY, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)


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


def get_scaled_pos(node_x, node_y, min_x, max_x, min_y, max_y, panel_rect, scale=1.0, padding=35):
    px, py, pw, ph = panel_rect
    
    # Calculate responsive padding and metrics height
    scaled_padding = int(padding * scale)
    line_spacing = max(14, int(20 * scale))
    box_padding = max(8, int(10 * scale))
    metrics_box_h = box_padding * 2 + line_spacing * 5
    
    # Leave space at top for title (approx 40 * scale) and bottom for metrics box
    title_height = int(40 * scale)
    
    draw_w = pw - 2 * scaled_padding
    draw_h = ph - 2 * scaled_padding - title_height - metrics_box_h
    
    dx = max_x - min_x
    dy = max_y - min_y
    if dx == 0: dx = 1
    if dy == 0: dy = 1

    scale_x = draw_w / dx
    scale_y = draw_h / dy
    scale_factor = min(scale_x, scale_y)

    # Center coordinates
    graph_w = dx * scale_factor
    graph_h = dy * scale_factor
    offset_x = px + scaled_padding + (draw_w - graph_w) / 2
    offset_y = py + scaled_padding + title_height + (draw_h - graph_h) / 2

    # Invert Y so larger Y values are higher up
    x_pos = offset_x + (node_x - min_x) * scale_factor
    y_pos = offset_y + (max_y - node_y) * scale_factor

    return int(x_pos), int(y_pos)


def get_path_cost(node_id, came_from, graph, origin):
    if node_id == origin:
        return 0
    cost = 0
    curr = node_id
    visited = set()
    while curr != origin and curr in came_from:
        if curr in visited:
            break
        visited.add(curr)
        parent = came_from[curr]
        if parent is None:
            break
        edge_cost = None
        if parent in graph:
            for neighbor_id, weight in graph[parent].neighbors:
                if neighbor_id == curr:
                    edge_cost = weight
                    break
        if edge_cost is None:
            break
        cost += edge_cost
        curr = parent
    return cost


def copy_state(state):
    if not state:
        return {}
    return {
        'current_node': state.get('current_node'),
        'visited': set(state.get('visited', set())),
        'frontier': set(state.get('frontier', set())),
        'came_from': dict(state.get('came_from', {})),
        'nodes_created': state.get('nodes_created', 0),
        'status': state.get('status', 'searching'),
        'path': list(state.get('path')) if state.get('path') is not None else None,
        'path_cost': state.get('path_cost', 0)
    }


def copy_sim_states(sim_states):
    return {name: copy_state(state) for name, state in sim_states.items()}


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
        # Window configuration - Fullscreen by default for all platforms
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        
        if self.width <= 0 or self.height <= 0:
            self.width = 1600
            self.height = 1000
            self.fullscreen = False
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        else:
            self.fullscreen = True
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            
        pygame.display.set_caption("Graph Search Visualizer — Side-by-Side Comparison")
        
        self.scale = min(self.width / 1400.0, self.height / 950.0)
        update_fonts(self.scale)
        
        self.clock = pygame.time.Clock()
        self.running = True

        # Scan for map files in the 'maps/' directory
        self.maps_dir = "maps"
        self.map_paths = []
        if os.path.exists(self.maps_dir):
            self.map_paths = sorted([os.path.join(self.maps_dir, f) for f in os.listdir(self.maps_dir) if f.endswith(".txt")])
        
        # Check command line arguments for a specific map file
        if len(sys.argv) > 1:
            arg_path = sys.argv[1]
            if os.path.exists(arg_path):
                abs_path = os.path.abspath(arg_path)
                if abs_path not in [os.path.abspath(p) for p in self.map_paths]:
                    self.map_paths.append(abs_path)
                    # Sort them by their basename for consistency
                    self.map_paths = sorted(self.map_paths, key=os.path.basename)
                # Find the index of the matched path
                for idx, path in enumerate(self.map_paths):
                    if os.path.abspath(path) == abs_path:
                        self.current_map_idx = idx
                        break
            else:
                print(f"Warning: Specified map file '{arg_path}' not found. Defaulting to available maps.")
                if not self.map_paths:
                    print("Error: No map text files found in the 'maps/' directory!")
                    pygame.quit()
                    sys.exit(1)
                self.current_map_idx = 0
        else:
            if not self.map_paths:
                print("Error: No map text files found in the 'maps/' directory!")
                pygame.quit()
                sys.exit(1)
            self.current_map_idx = 0

        self.current_map_path = self.map_paths[self.current_map_idx]

        # Algorithm Selection States
        # Order: BFS, DFS, GBFS, A*, CUS1, CUS2
        self.algo_selections = {
            "BFS": True,
            "DFS": True,
            "GBFS": True,
            "A*": True,
            "CUS1": True,
            "CUS2": True
        }

        # Simulation States
        self.sim_running = False
        self.sim_speed = 5  # steps per second
        self.last_step_time = 0
        self.show_heuristics = True
        self.history = []
        self.history_idx = 0
        
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

        # Error / Success feedback states
        self.ui_error_message = ""
        self.ui_error_time = 0.0

        # Custom Cross-Platform File Picker states
        self.show_file_picker = False
        self.picker_current_dir = os.path.abspath(".")
        self.picker_items = []
        self.picker_scroll_offset = 0
        self.picker_item_rects = []

        # Enable smooth keyboard repeats for text input (delay 500ms, repeat 50ms)
        pygame.key.set_repeat(500, 50)

        # Setup GUI controls
        self.setup_ui()

        # Load the initial map
        self.load_map_file()

    def setup_ui(self):
        sidebar_x = 20

        # 1. Map Input & Navigation (y: 90 to 220)
        self.btn_browse_map = Button(sidebar_x, 115, 280, 30, "Browse Map File...", COLOR_PANEL_BG, (30, 41, 59), callback=self.browse_file)
        self.btn_prev_map = Button(sidebar_x, 155, 45, 30, "<", COLOR_PANEL_BG, (30, 41, 59), callback=self.prev_map)
        self.btn_next_map = Button(sidebar_x + 235, 155, 45, 30, ">", COLOR_PANEL_BG, (30, 41, 59), callback=self.next_map)

        # 2. Algorithm Checkboxes (y: 235 to 450)
        self.checkboxes = []
        y_offset = 265
        for name in ["BFS", "DFS", "GBFS", "A*", "CUS1", "CUS2"]:
            cb = Checkbox(sidebar_x, y_offset, name, checked=self.algo_selections[name], 
                          callback=lambda val, n=name: self.toggle_algo(n, val))
            self.checkboxes.append(cb)
            y_offset += 30

        # 3. Speed Slider & Controls (y: 460 to 640)
        self.speed_slider = Slider(sidebar_x, 515, 280, 1, 60, self.sim_speed, "Speed (Steps/sec)", callback=self.set_speed)
        self.btn_back = Button(sidebar_x, 545, 85, 35, "Back", COLOR_PANEL_BG, (30, 41, 59), callback=self.step_back)
        self.btn_play_pause = Button(sidebar_x + 95, 545, 90, 35, "Play", (16, 185, 129), (52, 211, 153), callback=self.toggle_play)
        self.btn_step = Button(sidebar_x + 195, 545, 85, 35, "Next", COLOR_PANEL_BG, (30, 41, 59), callback=self.step_once)
        self.btn_reset = Button(sidebar_x, 590, 280, 35, "Reset Simulation", (239, 68, 68), (248, 113, 113), callback=self.reset_simulation)
        self.cb_show_heuristics = Checkbox(sidebar_x, 635, "Show Heuristics on Nodes", checked=self.show_heuristics, callback=self.toggle_heuristics)

    def set_ui_error(self, msg):
        self.ui_error_message = msg
        self.ui_error_time = time.time()

    def populate_picker_items(self):
        try:
            items = os.listdir(self.picker_current_dir)
            dirs = []
            files = []
            
            # Parent directory link
            parent_dir = os.path.abspath(os.path.join(self.picker_current_dir, ".."))
            dirs.append(("..", parent_dir, True))
            
            for item in sorted(items):
                if item.startswith('.'):
                    continue
                path = os.path.join(self.picker_current_dir, item)
                if os.path.isdir(path):
                    dirs.append((item + "/", path, True))
                elif item.endswith('.txt'):
                    files.append((item, path, False))
                    
            self.picker_items = dirs + files
            self.picker_scroll_offset = 0
        except Exception as e:
            print(f"Error populating file explorer items: {e}")
            self.picker_items = [("..", os.path.abspath(os.path.join(self.picker_current_dir, "..")), True)]

    def browse_file(self):
        # Open our custom cross-platform file picker modal
        self.show_file_picker = True
        if not os.path.exists(self.picker_current_dir):
            self.picker_current_dir = os.path.abspath(".")
        self.populate_picker_items()

    def load_custom_map_path(self, filepath):
        filepath = filepath.strip()
        if not filepath:
            self.set_ui_error("Empty path!")
            return
            
        target_path = None
        if os.path.exists(filepath):
            target_path = os.path.abspath(filepath)
        elif os.path.exists(os.path.join(self.maps_dir, filepath)):
            target_path = os.path.abspath(os.path.join(self.maps_dir, filepath))
            
        if target_path:
            try:
                # Validate by parsing
                load_map(target_path)
                
                # If valid, append and select
                if target_path not in [os.path.abspath(p) for p in self.map_paths]:
                    self.map_paths.append(target_path)
                    self.map_paths = sorted(self.map_paths, key=os.path.basename)
                    
                for idx, path in enumerate(self.map_paths):
                    if os.path.abspath(path) == target_path:
                        self.current_map_idx = idx
                        break
                self.current_map_path = target_path
                self.load_map_file()
                self.ui_error_message = ""
            except Exception as e:
                self.set_ui_error("Format Error!")
                print(f"Error validating map format: {e}")
        else:
            self.set_ui_error("File not found!")

    def load_map_file(self):
        filepath = self.current_map_path
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
            print(f"Error loading map file {os.path.basename(self.current_map_path)}: {e}")

    def prev_map(self):
        if self.map_paths:
            self.current_map_idx = (self.current_map_idx - 1) % len(self.map_paths)
            self.current_map_path = self.map_paths[self.current_map_idx]
            self.load_map_file()

    def next_map(self):
        if self.map_paths:
            self.current_map_idx = (self.current_map_idx + 1) % len(self.map_paths)
            self.current_map_path = self.map_paths[self.current_map_idx]
            self.load_map_file()

    def toggle_algo(self, name, checked):
        self.algo_selections[name] = checked
        self.reset_simulation()

    def set_speed(self, val):
        self.sim_speed = val

    def toggle_heuristics(self, val):
        self.show_heuristics = val

    def step_back(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.sim_states = copy_sim_states(self.history[self.history_idx])
            if self.sim_running:
                self.toggle_play()

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
        self.history = []
        self.history_idx = 0

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
        initial_states = {}
        for name in active_algos:
            gen_func = GENERATORS[name]
            self.simulators[name] = gen_func(self.graph, self.origin, self.destinations)
            
            # Get the initial setup state from generator
            try:
                state = next(self.simulators[name])
                self.sim_states[name] = state
                initial_states[name] = state
            except StopIteration:
                pass
        self.history.append(copy_sim_states(initial_states))

    def step_once(self):
        # If we are not at the end of history, step forward in history
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
            self.sim_states = copy_sim_states(self.history[self.history_idx])
            return

        # Advance each simulator by one step
        next_states = {}
        any_advancements = False
        for name in list(self.simulators.keys()):
            simulator = self.simulators[name]
            current_state = self.sim_states.get(name)
            
            if current_state and current_state['status'] != 'searching':
                next_states[name] = current_state
                continue
                
            try:
                state = next(simulator)
                next_states[name] = state
                any_advancements = True
            except StopIteration:
                next_states[name] = current_state
        
        if any_advancements:
            self.history.append(copy_sim_states(next_states))
            self.history_idx += 1
            self.sim_states = next_states
        else:
            # If no generator could advance, pause play
            if self.sim_running:
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

            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.width = max(1200, event.w)
                    self.height = max(850, event.h)
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
                    self.scale = min(self.width / 1400.0, self.height / 950.0)
                    update_fonts(self.scale)

            if self.show_file_picker:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left Click
                        # Check cancel button
                        if hasattr(self, 'picker_cancel_rect') and self.picker_cancel_rect.collidepoint(event.pos):
                            self.show_file_picker = False
                            return
                        
                        # Check list items click
                        for rect, path, is_dir in self.picker_item_rects:
                            if rect.collidepoint(event.pos):
                                if is_dir:
                                    self.picker_current_dir = path
                                    self.populate_picker_items()
                                else:
                                    self.load_custom_map_path(path)
                                    self.show_file_picker = False
                                return
                    elif event.button == 4:  # Scroll Up
                        self.picker_scroll_offset = max(0, self.picker_scroll_offset - 1)
                    elif event.button == 5:  # Scroll Down
                        max_offset = max(0, len(self.picker_items) - 12)
                        self.picker_scroll_offset = min(max_offset, self.picker_scroll_offset + 1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_file_picker = False
                    elif event.key == pygame.K_UP:
                        self.picker_scroll_offset = max(0, self.picker_scroll_offset - 1)
                    elif event.key == pygame.K_DOWN:
                        max_offset = max(0, len(self.picker_items) - 12)
                        self.picker_scroll_offset = min(max_offset, self.picker_scroll_offset + 1)
                continue

            # Keyboard shortcut handler (Escape to exit, F/F11 to toggle fullscreen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                elif event.key == pygame.K_f or event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        info = pygame.display.Info()
                        self.width = info.current_w
                        self.height = info.current_h
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.width = 1600
                        self.height = 1000
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
                    self.scale = min(self.width / 1400.0, self.height / 950.0)
                    update_fonts(self.scale)

            # Feed events to UI controls
            self.btn_browse_map.handle_event(event)
            self.btn_prev_map.handle_event(event)
            self.btn_next_map.handle_event(event)
            for cb in self.checkboxes:
                cb.handle_event(event)
            self.speed_slider.handle_event(event)
            self.btn_back.handle_event(event)
            self.btn_play_pause.handle_event(event)
            self.btn_step.handle_event(event)
            self.btn_reset.handle_event(event)
            self.cb_show_heuristics.handle_event(event)

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
        self.screen.blit(lbl_map, (20, 90))
        
        self.btn_browse_map.draw(self.screen)
        
        self.btn_prev_map.draw(self.screen)
        map_name_surf = FONT_UI.render(os.path.basename(self.current_map_path), True, COLOR_TEXT_PRIMARY)
        map_name_rect = map_name_surf.get_rect(center=(160, 170))
        self.screen.blit(map_name_surf, map_name_rect)
        self.btn_next_map.draw(self.screen)

        # Draw error message if present
        if self.ui_error_message:
            if time.time() - self.ui_error_time > 3.0:
                self.ui_error_message = ""
            else:
                err_surf = FONT_UI.render(self.ui_error_message, True, COLOR_NODE_GOAL)
                self.screen.blit(err_surf, (20, 195))

        # Separator line
        pygame.draw.line(self.screen, COLOR_BORDER, (20, 220), (300, 220), 1)

        # Draw Checkboxes
        lbl_algos = FONT_SECTION.render("SEARCH ALGORITHMS", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_algos, (20, 235))
        for cb in self.checkboxes:
            cb.draw(self.screen)

        # Separator line
        pygame.draw.line(self.screen, COLOR_BORDER, (20, 450), (300, 450), 1)

        # Speed Slider & Controls Section Title
        lbl_sim = FONT_SECTION.render("SPEED / SIMULATION", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_sim, (20, 460))
        
        # Speed Slider & Controls
        self.speed_slider.draw(self.screen)
        self.btn_back.disabled = (self.history_idx == 0)
        self.btn_back.draw(self.screen)
        self.btn_play_pause.draw(self.screen)
        self.btn_step.draw(self.screen)
        self.btn_reset.draw(self.screen)
        self.cb_show_heuristics.draw(self.screen)

        # Legend panel at bottom of sidebar (2-column layout to save vertical space)
        legend_y = max(670, self.height - 250)
        lbl_legend = FONT_SECTION.render("LEGEND", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_legend, (20, legend_y))
        
        legend_col1 = [
            ("Start Node", COLOR_NODE_START, True),
            ("Goal Node", COLOR_NODE_GOAL, True),
            ("Current Node", COLOR_NODE_CURRENT, True),
            ("Frontier Node", COLOR_NODE_FRONTIER, True)
        ]
        legend_col2 = [
            ("Explored Node", COLOR_NODE_VISITED, True),
            ("Unexplored Edge", COLOR_EDGE_UNEXPLORED, False),
            ("Final Path Edge", COLOR_EDGE_PATH, False)
        ]

        # Draw Col 1
        item_y = legend_y + 25
        for text, color, is_node in legend_col1:
            if is_node:
                pygame.draw.circle(self.screen, color, (30, item_y + 7), 6)
            else:
                pygame.draw.line(self.screen, color, (20, item_y + 7), (40, item_y + 7), 3)
            txt_surf = FONT_UI.render(text, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(txt_surf, (48, item_y))
            item_y += 24

        # Draw Col 2
        item_y = legend_y + 25
        for text, color, is_node in legend_col2:
            if is_node:
                pygame.draw.circle(self.screen, color, (175, item_y + 7), 6)
            else:
                pygame.draw.line(self.screen, color, (165, item_y + 7), (185, item_y + 7), 3)
            txt_surf = FONT_UI.render(text, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(txt_surf, (193, item_y))
            item_y += 24

        # =====================================================================
        # MAIN GRID DRAWING
        # =====================================================================
        main_rect = (320, 0, self.width - 320, self.height)
        active_algos = [name for name, sel in self.algo_selections.items() if sel]
        k = len(active_algos)

        if k == 0:
            # Show empty placeholder message
            msg_surf = FONT_TITLE.render("Please select at least one algorithm to visualize.", True, COLOR_TEXT_MUTED)
            msg_rect = msg_surf.get_rect(center=(320 + (self.width - 320) // 2, self.height // 2))
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
            if name == "CUS1":
                title_text += " (Dijkstra)"
            elif name == "CUS2":
                title_text += " (IDA*)"
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
                # Compute responsive node and edge sizes
                scaled_node_radius = max(8, int(13 * self.scale))
                scaled_arrow_size = max(5, int(8 * self.scale))

                # First pass: Draw edges
                for node_id, node in self.graph.items():
                    p1 = get_scaled_pos(node.x, node.y, self.min_x, self.max_x, self.min_y, self.max_y, rect, scale=self.scale)
                    
                    for neighbor_id, cost in node.neighbors:
                        p2 = get_scaled_pos(self.graph[neighbor_id].x, self.graph[neighbor_id].y, self.min_x, self.max_x, self.min_y, self.max_y, rect, scale=self.scale)
                        
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

                        scaled_edge_width = max(1, int(edge_width * self.scale))
                        draw_directed_edge(self.screen, p1, p2, edge_color, width=scaled_edge_width, node_radius=scaled_node_radius + 1, arrow_size=scaled_arrow_size)
                        
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
                            lbl_x += nx * 10 * self.scale
                            lbl_y += ny * 10 * self.scale
                        
                        # Draw small backdrop box for label readability
                        weight_surf = FONT_EDGE.render(str(cost), True, COLOR_TEXT_MUTED)
                        bg_rect = weight_surf.get_rect(center=(lbl_x, lbl_y))
                        pygame.draw.rect(self.screen, COLOR_BG, bg_rect.inflate(int(4 * self.scale), int(2 * self.scale)))
                        self.screen.blit(weight_surf, bg_rect)

                # Second pass: Draw Nodes
                for node_id, node in self.graph.items():
                    pos = get_scaled_pos(node.x, node.y, self.min_x, self.max_x, self.min_y, self.max_y, rect, scale=self.scale)
                    
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
                        pygame.draw.circle(self.screen, node_color, pos, scaled_node_radius + 3, width=2)

                    pygame.draw.circle(self.screen, node_color, pos, scaled_node_radius)
                    pygame.draw.circle(self.screen, COLOR_TEXT_PRIMARY, pos, scaled_node_radius, width=1)
                    
                    # Draw node number inside
                    num_surf = FONT_NODE.render(str(node_id), True, COLOR_TEXT_PRIMARY)
                    num_rect = num_surf.get_rect(center=pos)
                    self.screen.blit(num_surf, num_rect)

                    # Draw heuristic value above the node
                    if self.show_heuristics and self.destinations:
                        h_val = min(math.sqrt((node.x - self.graph[d].x) ** 2 + (node.y - self.graph[d].y) ** 2) for d in self.destinations)
                        
                        # Check if node has been reached/explored to calculate g(n)
                        is_reached = (node_id == self.origin) or (node_id in visited_set) or (node_id in frontier_set) or (node_id == current_node_id)
                        
                        if is_reached:
                            g_val = get_path_cost(node_id, came_from, self.graph, self.origin)
                            sum_val = g_val + h_val
                            
                            g_str = f"g={int(g_val)}" if g_val.is_integer() else f"g={g_val:.1f}"
                            g_surf = FONT_EDGE.render(g_str, True, COLOR_TEXT_MUTED)
                            
                            h_str = f"h={int(h_val)}" if h_val.is_integer() else f"h={h_val:.1f}"
                            h_surf = FONT_EDGE.render(h_str, True, COLOR_TEXT_MUTED)
                            
                            gh_str = f"g+h={int(sum_val)}" if sum_val.is_integer() else f"g+h={sum_val:.1f}"
                            gh_surf = FONT_EDGE.render(gh_str, True, (74, 222, 128))  # obvious neon green color
                            
                            w1, h1 = g_surf.get_size()
                            w2, h2 = h_surf.get_size()
                            w3, h3 = gh_surf.get_size()
                            
                            box_w = max(w1, w2, w3) + int(8 * self.scale)
                            box_h = h1 + h2 + h3 + int(8 * self.scale)
                            
                            box_x = pos[0] - box_w // 2
                            box_y = pos[1] - scaled_node_radius - box_h - int(4 * self.scale)
                            box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
                            
                            pygame.draw.rect(self.screen, COLOR_PANEL_BG, box_rect, border_radius=6)
                            pygame.draw.rect(self.screen, COLOR_BORDER, box_rect, width=1, border_radius=6)
                            
                            y_offset = box_y + int(3 * self.scale)
                            g_rect = g_surf.get_rect(center=(pos[0], y_offset + h1 // 2))
                            y_offset += h1 + int(1 * self.scale)
                            h_rect = h_surf.get_rect(center=(pos[0], y_offset + h2 // 2))
                            y_offset += h2 + int(1 * self.scale)
                            gh_rect = gh_surf.get_rect(center=(pos[0], y_offset + h3 // 2))
                            
                            self.screen.blit(g_surf, g_rect)
                            self.screen.blit(h_surf, h_rect)
                            self.screen.blit(gh_surf, gh_rect)
                        else:
                            h_str = f"h={int(h_val)}" if h_val.is_integer() else f"h={h_val:.1f}"
                            h_surf = FONT_EDGE.render(h_str, True, COLOR_TEXT_MUTED)
                            h_rect = h_surf.get_rect(center=(pos[0], pos[1] - scaled_node_radius - 10))
                            
                            pygame.draw.rect(self.screen, COLOR_PANEL_BG, h_rect.inflate(int(4 * self.scale), int(2 * self.scale)), border_radius=4)
                            pygame.draw.rect(self.screen, COLOR_BORDER, h_rect.inflate(int(4 * self.scale), int(2 * self.scale)), width=1, border_radius=4)
                            self.screen.blit(h_surf, h_rect)

            # =================================================================
            # STATS & METRICS DISPLAY OVERLAY
            # =================================================================
            # Calculate metrics box height and spacing dynamically
            line_spacing = max(14, int(20 * self.scale))
            box_padding = max(8, int(10 * self.scale))
            metrics_box_h = box_padding * 2 + line_spacing * 5
            metrics_box = pygame.Rect(px + 10, py + ph - metrics_box_h - 10, pw - 20, metrics_box_h)
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
            
            y_offset = metrics_box.top + box_padding
            self.screen.blit(stat_lbl_surf, (px + 20, y_offset))
            # Place status value next to label
            self.screen.blit(stat_val_surf, (px + 20 + stat_lbl_surf.get_width(), y_offset))

            # Nodes Created
            y_offset += line_spacing
            live_created = state.get('nodes_created', 0)
            node_str = f"Nodes Created: {live_created}"
            node_surf = FONT_METRICS.render(node_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(node_surf, (px + 20, y_offset))

            # Path cost
            y_offset += line_spacing
            cost_str = f"Path Cost: {official_cost if official_path else 'N/A'}"
            if official_cost == float('inf'):
                cost_str = "Path Cost: N/A (No solution)"
            cost_surf = FONT_METRICS.render(cost_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(cost_surf, (px + 20, y_offset))

            # Execution time
            y_offset += line_spacing
            time_str = f"CPU Exec Time: {official_time:.4f} ms"
            time_surf = FONT_METRICS.render(time_str, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(time_surf, (px + 20, y_offset))

            # Path list display
            y_offset += line_spacing
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
            self.screen.blit(path_surf, (px + 20, y_offset))

        # Draw a tiny info footer on the main screen
        # footer_surf = FONT_METRICS.render("Visualizer advances frame-by-frame dynamically. Start node has glowing outer ring.", True, COLOR_TEXT_MUTED)
        # self.screen.blit(footer_surf, (340, self.height - 25))

        # =====================================================================
        # CROSS-PLATFORM FILE PICKER MODAL OVERLAY
        # =====================================================================
        if self.show_file_picker:
            # Dim background
            dim_surf = pygame.Surface((self.width, self.height))
            dim_surf.set_alpha(200)
            dim_surf.fill((10, 15, 25))
            self.screen.blit(dim_surf, (0, 0))

            # Picker Container (responsive sizing and centering)
            pw = int(700 * self.scale)
            ph = int(600 * self.scale)
            px = (self.width - pw) // 2
            py = (self.height - ph) // 2
            dialog_rect = pygame.Rect(px, py, pw, ph)
            pygame.draw.rect(self.screen, COLOR_SIDEBAR_BG, dialog_rect, border_radius=12)
            pygame.draw.rect(self.screen, COLOR_BORDER_ACTIVE, dialog_rect, width=2, border_radius=12)

            # Title
            title_surf = FONT_TITLE.render("Select Map Text File", True, COLOR_TEXT_PRIMARY)
            self.screen.blit(title_surf, (px + int(30 * self.scale), py + int(25 * self.scale)))

            # Current Path
            path_text = f"Folder: {self.picker_current_dir}"
            # Truncate path dynamically if too long
            max_path_pixels = int(640 * self.scale)
            if FONT_UI.size(path_text)[0] > max_path_pixels:
                path_text = "..." + self.picker_current_dir[-45:]
                # Further truncate if needed
                while FONT_UI.size(path_text)[0] > max_path_pixels and len(path_text) > 10:
                    path_text = "..." + path_text[4:]
            path_surf = FONT_METRICS.render(path_text, True, COLOR_TEXT_MUTED)
            self.screen.blit(path_surf, (px + int(30 * self.scale), py + int(55 * self.scale)))

            # Horizontal divider line
            pygame.draw.line(self.screen, COLOR_BORDER, (px + int(30 * self.scale), py + int(80 * self.scale)), (px + pw - int(30 * self.scale), py + int(80 * self.scale)), 1)

            # Draw items list
            self.picker_item_rects.clear()
            list_y = py + int(95 * self.scale)
            visible_count = 12
            visible_items = self.picker_items[self.picker_scroll_offset : self.picker_scroll_offset + visible_count]
            
            mouse_pos = pygame.mouse.get_pos()
            item_h = int(35 * self.scale)
            item_margin = int(5 * self.scale)

            for idx, (name, path, is_dir) in enumerate(visible_items):
                item_rect = pygame.Rect(px + int(30 * self.scale), list_y + idx * item_h, pw - int(60 * self.scale), item_h - item_margin)
                is_hovered = item_rect.collidepoint(mouse_pos)
                
                # Draw hover background
                if is_hovered:
                    bg_col = (30, 41, 59) # Slate 800
                    pygame.draw.rect(self.screen, bg_col, item_rect, border_radius=6)
                    pygame.draw.rect(self.screen, COLOR_BORDER_ACTIVE, item_rect, width=1, border_radius=6)
                
                # Decide icon and text color
                if name.startswith(".."):
                    icon = "↩  "
                    color = COLOR_TEXT_MUTED
                elif is_dir:
                    icon = "📁  "
                    color = COLOR_NODE_FRONTIER
                else:
                    icon = "📄  "
                    color = COLOR_TEXT_PRIMARY

                item_text = icon + name
                text_surf = FONT_UI.render(item_text, True, color)
                self.screen.blit(text_surf, (item_rect.x + int(10 * self.scale), item_rect.y + (item_rect.height - text_surf.get_height()) // 2))
                
                self.picker_item_rects.append((item_rect, path, is_dir))

            # Scroll indicators / position footer
            if len(self.picker_items) > visible_count:
                scroll_str = f"Items {self.picker_scroll_offset + 1}-{min(self.picker_scroll_offset + visible_count, len(self.picker_items))} of {len(self.picker_items)} (Use Scroll Wheel or Up/Down arrows)"
                scroll_surf = FONT_EDGE.render(scroll_str, True, COLOR_TEXT_MUTED)
                self.screen.blit(scroll_surf, (px + int(30 * self.scale), py + ph - int(70 * self.scale)))

            # Cancel Button
            cancel_w = int(100 * self.scale)
            cancel_h = int(32 * self.scale)
            cancel_rect = pygame.Rect(px + pw - cancel_w - int(30 * self.scale), py + ph - cancel_h - int(13 * self.scale), cancel_w, cancel_h)
            self.picker_cancel_rect = cancel_rect
            is_cancel_hovered = cancel_rect.collidepoint(mouse_pos)
            cancel_col = (239, 68, 68) if not is_cancel_hovered else (248, 113, 113)
            pygame.draw.rect(self.screen, cancel_col, cancel_rect, border_radius=6)
            
            cancel_surf = FONT_UI.render("Cancel", True, COLOR_TEXT_PRIMARY)
            cancel_text_rect = cancel_surf.get_rect(center=cancel_rect.center)
            self.screen.blit(cancel_surf, cancel_text_rect)

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
