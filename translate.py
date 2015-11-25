import config 

def translate(message, context):
    results = db.select('translations', {'message':message}, where="message = $message", what="message, translation")
    

def get_translations(messages):
    pass #multiple select
