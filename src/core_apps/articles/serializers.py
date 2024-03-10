from rest_framework import serializers

class TagListField(serializers.Field): 
        ''' To get all the tags in a list '''
        def to_representation(self, value):
                return [tag.name for tag in value.all()]

        def to_internal_value(self, data):
                if not isinstance(data, list):
                        raise serializers.ValidationError('Expected a list of tags')
                
                all_tags = []
                for tag in data: 
                        tag = tag.strip()
                        # if the tag is now empty string after removing any trailing spaces, continue 
                        if not tag:
                                continue
                        all_tags.append(tag)
                return all_tags