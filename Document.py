class Document:
  PORTRAIT = 'portrait'
  LANDSCAPE = 'landscape'

  TWO_SIDED_LONG = 'two-sided-long-edge'
  TWO_SIDED_SHORT = 'two-sided-short-edge'
  ONE_SIDED = 'one-sided'

  LETTER = 'letter'
  TABLOID = 'tabloid'
  CUSTOM = 'custom'

  filePath = None
  params = {'copies': 1, 
            'scale': True, 
            'sides': TWO_SIDED_LONG, 
            'range': None, 
            'orientation': PORTRAIT,
            'size': LETTER,
            'size_length': None,
            'size_width': None
            }

  def __init__(self, filePathIn):
    self.filePath = filePathIn
      
  def __str__(self):
    return self.filePath