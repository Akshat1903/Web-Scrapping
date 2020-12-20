from bs4 import BeautifulSoup
import requests
import csv


html_text = requests.get(
    'https://www.medicinenet.com/diseases_and_conditions/alpha_w.htm').text
soup = BeautifulSoup(html_text, 'lxml')
topic_section = soup.find('div', class_='AZ_results')
topics = topic_section.find_all('li')
f = open("w.csv", "w")
fieldnames = ['Questions', 'Answer']
writer = csv.DictWriter(f, fieldnames)
writer.writeheader()

for topic in topics:
    topic_url = topic.a['href']
    topic_html = requests.get(topic_url).text
    soup_final = BeautifulSoup(topic_html, 'lxml')
    divs = soup_final.find_all("div", class_="apPage")
    for div in divs:
        div_wrapper = div.find_all('div', class_='wrapper')
        for x in div_wrapper:
            try:
                if 'facts' in x.h3.span.text:
                    continue
                question = x.h3.span.text
                print(f"Question - {question}")
                paras = x.find_all('p')
                final_answer = ''
                for para in paras:
                    answer = para.strings
                    final_ans = [repr(string) for string in answer]
                    final_ans = ''.join(final_ans)
                    final_ans = final_ans.replace(r'\n', '')
                    final_ans = final_ans.replace(r'\r', '')
                    final_answer += final_ans.strip()
                try:
                    lists = x.find_all('li')
                    list_text = [b.text for b in lists]
                    new_list = []
                    for text in list_text:
                        if '\n\nShare Your Story\n' in text:
                            text = ''
                        if 'Readers Comments' in text:
                            text = ''
                        new_list.append(text)
                    final_list = ' '.join(new_list)
                    final_answer = final_answer + ' ' + final_list
                    writer.writerows([
                        {'Questions': question, 'Answer': final_answer}
                    ])
                except:
                    writer.writerows([
                        {'Questions': question, 'Answer': final_answer}
                    ])
            except:
                continue
f.close()
