
import json
from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer): 
        charset = 'utf-8'
        
        def render(self, data, accepted_media_type=None, renderer_context=None):
                if renderer_context is None: 
                        status_code = 200 
                else: 
                        status_code = renderer_context.get('response').status_code
                
                # in case of DELETE request, the "data" will be None else "data" will hold queryset or error codes 
                if data is not None: 
                        errors = data.get('errors', None)
                else: 
                        errors = None
                # print('data : ', data)
                # if there are errors, then render as per default JSON style. 
                if errors is not None: 
                        return super(ArticleJSONRenderer, self).render(data)
                else: 
                        if 'author_details' in data: 
                                author_details = data.pop('author_details')
                                return json.dumps({'status_code' : status_code, 'author_details' : author_details, 'article' : data})
                        
                        return json.dumps({'status_code' : status_code, 'article' : data})

               

# for articles => *s 
class ArticlesJSONRenderer(JSONRenderer): 
        charset = 'utf-8'
        
        def render(self, data, accepted_media_type=None, renderer_context=None):
                if renderer_context is None: 
                        status_code = 200 
                else: 
                        status_code = renderer_context.get('response').status_code
                
                errors = data.get('errors', None)
                
                
                
                # if there are errors, then render as per default JSON style. 
                if errors is not None: 
                        return super(ArticlesJSONRenderer, self).render(data)
                else: 
                        if 'author_details' in data: 
                                author_details = data.pop('author_details')
                                return json.dumps({'status_code' : status_code, 'author_details' : author_details, 'articles' : data})
                        
                        return json.dumps({'status_code' : status_code, 'articles' : data})

