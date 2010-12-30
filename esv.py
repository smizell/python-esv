import urllib

class ESVWebServiceAPI:
    """
    This is a class for accessing the ESV Bible API provided by Crossway.
    It works with version 2 of their API.
    
    Visit http://www.esvapi.org/api to view the full API
    """
    
    # Options for outputs
    
    base_options = {
        'key': 'IP',
    }
    
    html_options = {
        'include-passage-references': 'true',
        'include-first-verse-numbers': 'true',
        'include-verse-numbers': 'true',
        'include-footnotes': 'true',
        'include-footnote-links': 'true',
        'include-headings': 'true',
        'include-subheadings': 'true',
        'include-surrounding-chapters': 'false',
        'include-word-ids': 'true',
        'link-url': 'http://www.gnpcb.org/esv/search/',
        'include-audio-link': 'true',
        'audio-format': 'flash',
        'audio-version': 'hw',
        'include-short-copyright': 'true',
        'include-copyright': 'false',
    }

    xml_options = {
        'include-xml-declaration': 'false',
        'include-doctype': 'true',
        'include-quote-entities': 'true',
        'include-simple-entities': 'false',
        'include-cross-references': 'false',
        'include-line-breaks': 'true',
        'include-word-ids': 'false',
        'include-virtual-attributes': 'false',
        'base-element': 'verse-unit',
        'output-format': 'crossway-xml-1.0',
    }

    plain_text_options = {
        'include-passage-references': 'true',
        'include-first-verse-numbers': 'true',
        'include-verse-numbers': 'true',
        'include-footnotes': 'true',
        'include-short-copyright': 'true',
        'include-copyright': 'false',
        'include-passage-horizontal-lines': 'true',
        'include-heading-horizontal-lines': 'true',
        'include-headings': 'true',
        'include-subheadings': 'true',
        'include-selahs': 'true',
        'include-content-type': 'true',
        'line-length': 74,
        'output-format': 'plain-text',
    }

    mp3_options = {
        'output-format': 'mp3'
    }
    
    # Options for functions
    
    query_options = {
        'q': None,
        'passage': None,
        'words': None,
        'phrase': None,
        'not-words': None,
        'scope': None,
        'matches': None,
        'search-text': None,
        'page': None,
        'link-url': None,
        'results-per-page': None,
    }
    
    passage_query_options = query_options
    
    query_info_options = {
        'q': None,
    }
    
    reading_plan_query_options = {
        'date': None,
        'reading-plan': None,
        'start-date': None,
    }
    
    reading_plan_info_options = {
        'date': None,
        'reading-plan': None,
        'start-date': None,
    }
    
    verse_options = {
        'passage': None,
        'seed': None,
    }
    
    daily_verse_options = {
        'include-headings': 'false',
        'begin-character': '',
        'correct-capitalization': 'true',
        'correct-end-punctuation': 'true',
        'end-character': '&ellipsis4;',
        'correct-quotes': 'true'
    }
    
    def __init__(self, key='IP', base_url='http://www.esvapi.org/v2/rest/'):
        self.key = key
        self.base_options['key'] = key
        
        self.base_url = base_url
        
        # Outputs allowed through the API
        self.outputs = {
            'html': self.html_options,
            'xml': self.xml_options,
            'plain-text': self.plain_text_options,
            'mp3': self.mp3_options,
        }
        
        # Functions for this class and their corresponding REST call URLs
        self.function_names = {
            'query': 'query',
            'query_info': 'queryInfo',
            'passage_query': 'passageQuery',
            'reading_plan_query': 'readingPlanQuery',
            'reading_plan_info': 'readingPlanInfo',
            'verse': 'verse',
            'daily_verse': 'dailyVerse',
        }
        
        # Build the function dict
        self.functions = self._build_functions()
        
    def _build_functions(self):
        f = {}
        
        # Loop through the function names and build dict
        for k,v in self.function_names.items():
            f[k] = {'function': k,
                    'name': v,
                    'options': getattr(self, '%s_options' % k)}
            
        return f
        
        
    def _build_format_options(self, format, **kwargs):
        """
        Build the options for the specified format, such as
        plain-text, xml, or html
        """
        format_options = self.outputs[format]
        options = {}
        
        # Loop through all of the keywords, change underscores to dashes, build dict
        for k,v in kwargs.items():
            option = k.replace("_", "-")
            if format_options.has_key(option):
                # No reason to include default values
                if format_options[option] != v:
                    options[option] = v
        
        # The output-format is the only option required from these format options.
        if format_options.has_key('output-format'):
            options['output-format'] = format_options['output-format']
            
        return options
        
    def _build_function_options(self, function_options, **kwargs):
        """
        Builds the options based on the specific function options
        """
        options = {}
        
        # Loop through all of the keywords, change underscores to dashes, build dict
        for k,v in kwargs.items():
            option = k.replace("_", "-")
            if function_options.has_key(option):
               options[option] = v
               
        return options
        
    def _build_url(self, options, function_name):
        """
        Builds the URL from the options
        """
        options = urllib.urlencode(options)
        return "%s%s?%s" % (self.base_url, function_name, options)
        
    def _convert_kwargs(self, kwargs):
        for k,v in kwargs.items():
            if v is True:
                kwargs[k] = 'true'
            if v is False:
                kwargs[k] = 'false'
        return kwargs
        
    def _get_response(self, format, function, **kwargs):
        """
        Gets the response from the API
        """
        function = self.functions[function]
        
        kwargs = self._convert_kwargs(kwargs)
        
        # Create dictionaries of the optional arguments
        options = function['options'] # These are the options for the specific function called
        function_options = self._build_function_options(options, **kwargs)
        format_options = self._build_format_options(format, **kwargs)
        
        # Combine all of the options from above
        all_options = dict(function_options.items() + format_options.items() + self.base_options.items())
        
        # Build the URL from all combined options
        url = self._build_url(all_options, function['name'])
        print url
        
        return urllib.urlopen(url)
        
    # Functions 
        
    def query(self, **kwargs):
        """
        query function for ESV API
        
        Returns only HTML
        """
        return self._get_response('html', 'query', **kwargs)
        
    def query_info(self, **kwargs):
        """
        queryInfo function for ESV API
        
        Returns only XML
        """
        return self._get_response('xml', 'query_info', **kwargs)
        
    def passage_query(self, format='html', **kwargs):
        """
        passageQuery function for ESV API
        """
        return self._get_response(format, 'passage_query', **kwargs)
        
    def reading_plan_query(self, format='html', **kwargs):
        """
        readingPlanQuery function for ESV API
        """
        return self._get_response(format, 'reading_plan_query', **kwargs)
        
    def reading_plan_info(self, **kwargs):
        """
        readingPlanInfo function for ESV API
        """
        return self._get_response('xml', 'reading_plan_info', **kwargs)
        
    def verse(self, format='html', **kwargs):
        """
        verse function for ESV API
        """
        return self._get_response(format, 'verse', **kwargs)
        
    def daily_verse(self, format='html', **kwargs):
        """
        dailyVerse function for ESV API
        """
        return self._get_response(format, 'daily_verse', **kwargs)
        
if __name__ == '__main__':
    e = ESVWebServiceAIP(key='TEST')
    print e.passage_query(passage='John 3').read()
