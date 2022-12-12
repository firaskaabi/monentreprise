import requests
from bs4 import BeautifulSoup
import tkinter as tk
import csv
import PyPDF2
import re

def uploadPdf():
    URL = "https://monentreprise.bj/page/annonces?Company_page=46&ajax=annonces-list"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    nextPage=soup.find('li', class_ = "next")
    urlNextpage=nextPage.find('a')['href'];
    print(urlNextpage)
    i=0;
    traite=True;
    while(traite):
        for annonce in soup.select('h5[class*="text-primary text-uppercase"]'):
            href=annonce.find('a')['href']
            i += 1
            print("Downloading file: ", i)
            response = requests.get(href)
            pdf = open("./pdf/annonce"+str(i)+".pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
        pos=URL.index('/page/anno')
        pageEnCour=URL[pos:]
        URL = "https://monentreprise.bj"+urlNextpage
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        nextPage=soup.find('li', class_ = "next")
        urlNextpage=nextPage.find('a')['href']
        print(urlNextpage)
        print(pageEnCour)
        if(pageEnCour==urlNextpage):
            traite=False
def ExtractData():
    dénomination=''
    objet=''
    capitalSocial=''
    siegeSocial=''
    greant=''
    rccm=''
    durée=''
    depot=''
    date=''
    gener=''
    nom=''
    prenom=''
    data=[]
    with open('data.csv', 'w') as file:
        header = ["DENOMINATION SOCIALE","OBJET", "CAPITAL SOCIAL", "SIEGE SOCIAL","RCCM","Durée","Dépôt au Greffe","DATE", "GERANT(E) NOM","GERANT(E) PRENOM", "GENER"]
        writer = csv.writer(file)
        writer.writerow(header)
    for j in range(1):
        pdfPath="./pdf/annonce"+str((j+1))+".pdf"
        print(pdfPath)
        pdfFileObj = open(pdfPath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        pageObj = pdfReader.getPage(0)
        info = pageObj.extractText()
        if(pdfReader.numPages==2):
            pageObj=pdfReader.getPage(1)
            info+="\n"+pageObj.extractText()
        arrayInfo = info.splitlines()
        for f in range(len(arrayInfo)-1):
            print(arrayInfo[f])
            if(re.match('^Dénomination',arrayInfo[f])):
                dénomination=arrayInfo[f+1]
            if(re.match('^Objet',arrayInfo[f])):
                l=1;
                while(not(re.match('^Capital Social',arrayInfo[f+l]))):
                    if(not(re.match('^Siège APIEX',arrayInfo[f+l])) and not(re.match('^Bénin - Tél',arrayInfo[f+l]))):
                        objet+=' '+arrayInfo[f+l]
                    l=l+1
            if(re.match('^Capital Social:',arrayInfo[f])):
                l=1;
                while(not(re.match('^Siège Social',arrayInfo[f+l]))):
                    if(not(re.match('^Siège APIEX',arrayInfo[f+l])) and not(re.match('^Bénin - Tél',arrayInfo[f+l]))):
                        capitalSocial+=' '+arrayInfo[f+l]
                    l=l+1
            if(re.match('^Siège Social:',arrayInfo[f])):
                l=1;
                while(not(re.match('^Gérant',arrayInfo[f+l]))):
                    if(not(re.match('^Siège APIEX',arrayInfo[f+l])) and not(re.match('^Bénin - Tél',arrayInfo[f+l]))):
                        siegeSocial+=' '+arrayInfo[f+l]
                    l=l+1
            if(re.match('^Gérant:',arrayInfo[f])):
                greant=arrayInfo[f+1]
            if(re.match('^RCCM:',arrayInfo[f])):
                rccm=arrayInfo[f+1]
            if(re.match('^Durée:',arrayInfo[f])):
                durée=arrayInfo[f+1]
            if(re.match('^Dépôt au Greffe:',arrayInfo[f])):
                depot=arrayInfo[f+1]

        pos=greant.find(' ')
        gener=greant[:pos]
        greant=greant[(pos+1):]
        pos=greant.find(' ')
        nom=greant[:pos]
        greant=greant[(pos+1):]
        print(nom)
        pos=greant.find(' ')
        prenom=greant[:pos]
        print(prenom)
        pos=rccm.find(' du ')
        date=rccm[pos:]
        rccm=rccm[:pos]
        date=date.replace(' du ','')
        pos=depot.find(' du ')
        depot=depot[:pos]
        print(rccm)
        data = [dénomination,objet,capitalSocial, siegeSocial, rccm,durée,depot,date, nom, prenom,  gener]
        with open('data.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
root= tk.Tk()
label1 = tk.Label(text='')
label1.pack(padx=2,pady=2)
button1 = tk.Button(text='upload pdf ', command=uploadPdf, bg='brown', fg='white')
button1.pack(padx=2, pady=5)
button2 = tk.Button(text='Extract Data', command=ExtractData, bg='brown', fg='white')
button2.pack(padx=6, pady=10)
root.geometry("600x400")
root.resizable(width=False, height=False)
root.title("Extraction de donnee PDF")
root.mainloop()

