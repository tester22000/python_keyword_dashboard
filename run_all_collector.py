if __name__ == '__main__':
    import sys
    from os import getcwd
    from os.path import dirname

    from app.link_title_collector import collect_titles
    from app.link_keyword_collector import extract_keywords
    from app.link_title_scoring import  link_title_scoring

    work_directory = dirname(__file__);
    sys.path.append(work_directory)

    collect_titles('./config/site_source.yaml')
    extract_keywords('./config/llm_config.yaml')
    link_title_scoring()
    