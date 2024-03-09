
import json
from rest_framework.renderers import JSONRenderer


class ArticleRenderer(JSONRenderer): 
        charset = 'utf-8'
        
        def render(self, data, accepted_media_type=None, renderer_context=None):
                if renderer_context is None: 
                        status_code = 200 
                else: 
                        status_code = renderer_context.get('response').status_code
                
                errors = data.get('errors', None)
                
                # if there are errors, then render as per default JSON style. 
                if errors is not None: 
                        return super(ArticleRenderer, self).render(data)
                # else, render in the below way in JSON 
                return json.dumps({'status_code' : status_code, 'article' : data})

# for articles => *s 
class ArticlesRenderer(JSONRenderer): 
        charset = 'utf-8'
        
        def render(self, data, accepted_media_type=None, renderer_context=None):
                if renderer_context is None: 
                        status_code = 200 
                else: 
                        status_code = renderer_context.get('response').status_code
                
                errors = data.get('errors', None)
                
                # if there are errors, then render as per default JSON style. 
                if errors is not None: 
                        return super(ArticlesRenderer, self).render(data)
                # else, render in the below way in JSON 
                return json.dumps({'status_code' : status_code, 'articles' : data})

