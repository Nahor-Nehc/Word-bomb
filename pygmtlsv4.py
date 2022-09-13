import pygame

class Button:
  """
  This class holds every button instance created by the create function
  """
  def __init__(self):
    self.buttons = []
    self.visible = []
    self.hidden = []
    
    self.attrs = {
      "rect" : 0,
      "colour" : 1,
      "event" : 2,
      "outlineWidth" : 3,
      "outlineColour" : 4,
      "text" : 5,
      "font" : 6,
      "textColour" : 7,
    }
    
  def create(self, rect, colour, event, outlineWidth = 0, outlineColour = (0, 0, 0), visible = True, text = "", font = None, textColour = (0, 0, 0)):
    """
    This function creates a button
    
    :param rect: the rectangle of the button
    :type rect: pygame.Rect
    
    :param colour: the colour of the rectangle
    :type colour: (R, G, B)
    
    :param event: event called by clicking on the button
    :type event: pygame.USEREVENT
    
    :param outlineWidth: the width of the outline
    :type int: integer
    
    :param outlineColour: the colour of the border
    :type outlineColour: (R, G, B)
    """
    temp = [rect, colour, event, outlineWidth, outlineColour, text, font, textColour]
    if visible == True:
      self.visible.append(temp)
    else:
      self.hidden.append(temp)
    self.buttons.append(temp)

  def draw(self, window):
    for button in self.visible:
      pygame.draw.rect(window, button[self.attrs["colour"]], button[self.attrs["rect"]])
      if button[self.attrs["outlineWidth"]] != 0:
        pygame.draw.rect(window, button[self.attrs["outlineColour"]], button[self.attrs["rect"]], button[self.attrs["outlineWidth"]])
      if button[self.attrs["font"]] != None:
        txt = button[self.attrs["font"]].render(button[self.attrs["text"]], 1, button[self.attrs["textColour"]])
        window.blit(txt, (button[self.attrs["rect"]].centerx - txt.get_width()/2, button[self.attrs["rect"]].centery - txt.get_height()/2))
      
  def check(self, mouse):
    for button in self.visible:
      if button[self.attrs["rect"]].collidepoint(mouse):
        pygame.event.post(pygame.event.Event(button[self.attrs["event"]]))
        
  def toggleVis(self, rect):
    edited = False
    for button in self.visible:
      if button[self.attrs["rect"]] == rect:
        self.visible.remove(button)
        self.hidden.append(button)
        edited = True
        
    if edited == False:
      for button in self.hidden:
        if button[self.attrs["rect"]] == rect:
          self.hidden.remove(button)
          self.visible.append(button)
      
  def changeAttr(self, rect, attr, newVal):
    if attr in self.attrs.keys():
      for button in self.buttons:
        if button[self.attrs["rect"]] == rect:
          button[self.attrs[attr]] = newVal
    else:
      raise ValueError("Attribute does not exist: " + str(attr))
    
  def remove(self, rect):
    for button in self.buttons:
      if button[self.attrs["rect"]] == rect:
        self.buttons.remove(button)
        try:
          self.hidden.remove(button)
        except:
          self.visible.remove(button)


class Scroll:
  def __init__(self, x, y, width, height, maxHeight, scrollbarWidth, colour):
    self.buffer = 2
    
    self.currentY = 0
    
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.total = maxHeight
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.surface = pygame.Surface((self.width, self.height))
    self.colour = colour
    
    self.surface.fill(self.colour)
    
    self.scrollClickY = 0
    
    self.scrollBar = [self.width - scrollbarWidth - self.buffer, self.height*(self.currentY/self.total) + self.buffer, scrollbarWidth, (self.height/self.total)*self.height - self.buffer*2]
    self.scrollBarRect = pygame.Rect(*self.scrollBar)
    self.down = False
    
    self.items = []
    
  def draw(self, window):
    window.blit(self.surface, (self.x, self.y))
    pygame.draw.rect(self.surface, self.colour, pygame.Rect(0, 0, self.width, self.height))
    for item in self.items:
      if item["shape"] == "rect":
        pygame.draw.rect(self.surface, item["colour"], pygame.Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]))
        if item["borderWidth"] != None and item["borderColour"] != None:
          pygame.draw.rect(self.surface, item["borderColour"], pygame.Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]), item["borderWidth"])
          
      elif item["shape"] == "line":
        pygame.draw.aaline(self.surface, item["colour"], (item["start"][0], item["start"][1]-self.currentY), (item["end"][0], item["end"][1]-self.currentY), item["width"])
        
      elif item["shape"] == "circle":
        pygame.draw.circle(self.surface, item["colour"], (item["centerx"], item["centery"] - self.currentY), item["radius"])
        if item["borderWidth"] != None and item["borderColour"] != None:
          pygame.draw.circle(self.surface, item["borderColour"], (item["centerx"], item["centery"] - self.currentY), item["radius"], item["borderWidth"])
          
      elif item["shape"] == "surface":
        pass
    
    pygame.draw.rect(self.surface, (211, 211, 211), self.scrollBarRect)
    
    self.items = []

  def draw_rect(self, rect_name, colour, x, y, width, height, borderWidth=None, borderColour=None):
    dictionary = {
      "shape" : "rect",
      "name" : rect_name,
      "colour" : colour,
      "x" : x,
      "y" : y,
      "width" : width,
      "height" : height,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)
    
  def draw_line(self, line_name, colour, start, end, width):
    dictionary = {
      "shape" : "line",
      "name" : line_name,
      "colour" : colour,
      "start" : start,
      "end" : end,
      "width" : width
    }
    self.items.append(dictionary)
    
  def draw_circle(self, line_name, colour, centerx, centery, radius, borderWidth = None, borderColour = None):
    dictionary = {
      "shape" : "circle",
      "name" : line_name,
      "colour" : colour,
      "centerx" : centerx,
      "centery" : centery,
      "radius" : radius,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)

  def blit(self, surface, destination):
    dictionary = {
      "shape" : "surface",
      
    }
    
    self.items.append(dictionary)
    
  
  
  def checkMouseDown(self, mouse):
    rect = pygame.Rect(self.scrollBarRect.left + self.x, self.scrollBarRect.top + self.y, self.scrollBarRect.width, self.scrollBarRect.height)
    if rect.collidepoint(mouse):
      self.scrollClickY = mouse[1]
      self.down = True
      self.origin = self.scrollBarRect[1]
      
  def checkMouseMotion(self, mouse):
    if pygame.mouse.get_pressed()[0] and self.down == True:
      self.currentY = self.origin + mouse[1] - self.scrollClickY
      
      if self.currentY < self.buffer:
        self.currentY = self.buffer
        
      elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
        self.currentY = self.height - self.scrollBarRect.height - self.buffer
      self.scrollBar[1] = self.currentY
      self.scrollBarRect = pygame.Rect(*self.scrollBar)
        
  def checkMouseUp(self, mouse):
    self.scrollClickY = 0
    self.down = False

  def checkScroll(self, event, sensitivity=5):
    self.currentY -= sensitivity*event.y
    if self.currentY < self.buffer:
      self.currentY = self.buffer

    elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
      self.currentY = self.height - self.scrollBarRect.height - self.buffer
      
    self.scrollBar[1] = self.currentY
    self.scrollBarRect = pygame.Rect(*self.scrollBar)
    
class Menu:
  class header:
    def __init__(self, bgcolour, fgcolour, textcolour, x, y, width, height, headings, font, padding, outlinecolour=(0, 0, 0)):

      self.bgcolour = bgcolour
      self.fgcolour = fgcolour
      self.textcolour = textcolour
      self.outlinecolour = outlinecolour
      self.font = font
      self.padding = padding
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.headings = headings
      self.current = 0
      
    def setCurrent(self, current):
      self.current = current
      
    def incrementCurrent(self):
      self.current += 1
      if self.current >= len(self.headings):
        self.current = 0
        
    def decrementCurrent(self):
      self.current -= 1
      if self.current < 0:
        self.current = len(self.headings) - 1
      
    def draw(self, window):
      pygame.draw.rect(window, self.bgcolour, pygame.Rect(self.x, self.y, self.width, self.height))
      pygame.draw.line(window, self.outlinecolour, (0, self.y + self.height), (self.width, self.y + self.height))
      totalLen = self.x + 5
      for heading in self.headings:
        text = self.font.render(heading.upper(), 1, self.textcolour)
        if self.headings.index(heading) == self.current:
          pygame.draw.rect(window, self.outlinecolour, pygame.Rect(totalLen, self.y, text.get_width()+self.padding, self.height-1), 1)
          pygame.draw.rect(window, self.fgcolour, pygame.Rect(totalLen + 1, self.y + 1, text.get_width()+self.padding - 2, self.height-2))
        else:
          pygame.draw.rect(window, self.outlinecolour, pygame.Rect(totalLen, self.y + self.padding/5, text.get_width()+ self.padding, self.y + self.height+1-self.padding/5), 1)
        window.blit(text, (totalLen + self.padding/2, (self.y*2 + self.height-text.get_height())/2))
        totalLen += text.get_width()+self.padding-1

class Animation_group:
  def __init__(self):
    self.animations = []
    
  def get_animations(self, display = True):
    if display == True:
      print(self.animations)
    return self.animations
    
  def set_animations(self, animations):
    self.animations = animations
    
  def add_animation(self, animation_object):
    self.animations.append(animation_object)

  def play_all(self, window, auto_increment_frame, auto_stop = False):
    for animation in self.animations:
      animation.play(window, auto_increment_frame, auto_stop)
  
  def play(self, animation_object, window,auto_increment_frame, auto_stop = False):
    animation_object.play(window, auto_increment_frame, auto_stop)
    
  def create_animation(self, x, y, frame_type = "image"):
    self.animations.append(Animation(x, y, frame_type))
    
  def remove_animation(self, animation_object_or_index):
    if isinstance(int, animation_object_or_index):
      self.animations.pop(animation_object_or_index)
    else:
      self.animations.remove(animation_object_or_index)
      
  def start_all(self):
    for anims in self.animations:
      anims.start()
      
  def stop_all(self):
    for anims in self.animations:
      anims.stop()

class Animation:
  def __init__(self, x, y, frame_type = "image"):
    self.initial_x = x
    self.initial_y = y
    self.current_x = x
    self.current_y = y
    self.frames = []
    self.offsets = []
    self.type = frame_type
    self.current = 0
    self.state = "stop"
    
  def start(self):
    
    # allows the play function to run
    self.state = "playing"
    
  def stop(self):
    # prevents the play function from running
    self.state = "stop"
    
  def set_coords(self, initial_x, initial_y, current_x, current_y):
    # allows the user to change the coords
    self.initial_x = initial_x
    self.initial_y = initial_y
    self.current_x = current_x
    self.current_y = current_y
    
  def get_coords(self, display = True):
    if display == True:
      print("%s, %s" %(self.initial_x, self.initial_y))
    return self.initial_x, self.initial_y
    
  def get_frames(self, display = True):
    if display == True:
      print(self.frames)
    return self.frames
  
  def set_frames(self, frames = []):
    self.frames = frames
    
  def get_offsets(self, display = True):
    if display == True:
      print(self.offsets)
    return self.offsets
  
  def set_offsets(self, offsets = []):
    self.offsets = offsets
    
  def duplicate_frame(self, frame_index, duplication_factor = 2):
    
    # gets the frame and offset
    frame = self.frames[frame_index]
    offset = self.offsets[frame_index]
    
    # gets the current range of frames
    frames = self.frames
    offsets = self.offsets
    
    # point of duplication
    for _ in range(0, duplication_factor):
      frames.insert(frame_index, frame)
      offsets.insert(frame_index, offset)
    
    # uploads the changes to the 
    self.set_frames(frames)
    self.set_offsets(offsets)
    
  def duplicate_range(self, index_list, duplication_factor = 2):
    
    # reverses the index list to prevent duplicating the incorrect 
    index_list.sort(reverse = True)
    for index in index_list:
      self.duplicate_frame(index, duplication_factor)
    
  def duplicate_all_frames(self, duplication_factor = 2):
    
    self.duplicate_range([x for x in range(0, len(self.frames))], duplication_factor)
    
    # frames = []
    # offsets = []
    # [frames.extend([frame for _ in range(duplication_factor)]) for frame in self.frames]
    # [offsets.extend([offset for _ in range(duplication_factor)]) for offset in self.offsets]
    # self.set_frames(frames)
    # self.set_offsets(offsets)

  def get_current_frame(self, display = True):
    if display == True:
      print(self.current)
    return self.current
  
  def set_current_frame(self, frame):
    self.current = frame
    
  def increment_frame(self):
    self.current += 1
    if self.current >= len(self.frames):
      self.current = 0
  
  def decrement_frame(self):
    self.current -= 1
    if self.current < 0:
      self.current = len(self.frames) - 1
    
  def add_frame(self, image, offset = [0, 0]):
    self.frames.append(image)
    self.offsets.append(offset)
    
  def remove_frame(self, index):
    self.frames.pop(index)
    self.offsets.pop(index)
    
  def play_next_frame(self, window, auto_increment_frame = True, auto_stop = False):
    if self.state == "playing":
      if self.type == "image":
        
        # adjusts image position
        self.current_x += self.offsets[self.current][0]
        self.current_y += self.offsets[self.current][1]
        
        # draws image on screen
        window.blit(self.frames[self.current], (self.current_x, self.current_y))
        
        if auto_stop == True:
          if self.current == len(self.frames) - 1:
            self.stop()
        
        #moves frame forwards by 1
        if auto_increment_frame == True:
          self.increment_frame()
      #if self.type == ""

  def play(self, window, auto_increment_frame, auto_stop = False):
    self.play_next_frame(window, auto_increment_frame, auto_stop)
