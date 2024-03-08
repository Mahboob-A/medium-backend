import re 
from math import ceil



class ArticleReadTimeEngine: 
        ''' 
        Class to help determine probable reading time of an article by an user
        A general assumption us that 200 words per minutes is taken for an average reading time. 
        '''
        @staticmethod
        def word_count(text): 
                words = re.findall(f"r\w+", text)
                return len(words)
        
        @staticmethod
        def estimate_reading_time(text, words_per_minute=200, seconds_per_image=7, seconds_per_tag=1): 
                title_word_count = ArticleReadTimeEngine.word_count(text)
                body_word_count = ArticleReadTimeEngine.word_count(text)
                description_word_count = ArticleReadTimeEngine.word_count(text)
        
                total_word_count = title_word_count + body_word_count + description_word_count 
                
                reading_time = total_word_count / words_per_minute 
                
                if text.has_banner_image: 
                        reading_time += seconds_per_image 
                
                if text.has_body_image_1: 
                        reading_time += seconds_per_image 
                        
                if text.has_body_image_2: 
                        reading_time + seconds_per_image 
                
                if text.has_body_image_3: 
                        reading_time + seconds_per_image 
                        
                total_tags = text.tags.count()
                
                if total_tags > 0: 
                        reading_time += total_tags * seconds_per_tag
                        
                reading_time = ceil(reading_time)
                
                return reading_time