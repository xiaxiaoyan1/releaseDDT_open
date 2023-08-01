from jinja2 import Environment,FileSystemLoader
import os.path


def generate_html(body,timelist,versiondic):
    path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates')
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template('Htmlmode.html')
    html_content = template.render(start_time = timelist['start_time'],
                                   end_time = timelist['end_time'],
                                   version = versiondic['version'],
                                   ispass = versiondic['ispass'],
                                   isfail = versiondic['isfail'],
                                   pass_rate = versiondic['pass_rate'],
                                   body = body)
    return html_content

def htmlresport(fail_list,timelist,versiondic):
    body = []
    for i in range(len(fail_list)):
        body.append(fail_list[i])
    html_content = generate_html(body = body, timelist = timelist, versiondic = versiondic)
    return html_content




