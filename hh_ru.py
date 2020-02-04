from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
import cx_Oracle
import traceback
import re

def hh_ru(browser, browser1, vKeyWord):
    try:
        soup = BeautifulSoup(browser.page_source)
        con = cx_Oracle.connect('skorkinyl/rjnjhsq1980@10.36.131.4/sigmadb')
        cur = con.cursor()
        sql = "insert into hh_work (keyWord, vak_name, vak_sal, vak_id, vak_text, vLink, rekr_link, rekr_name, emp_addr, sdata) values (:pkeyWord, :pvak_name, :pvak_sal, :pvak_id, :pvak_text, :pLink, :prekr_link, :prekr_name, :pemp_addr, :psdata)"

        #vakans = browser.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div[*]")
        vakans = soup.find_all("a", class_="bloko-link HH-LinkModifier")
        #wait = WebDriverWait(browser, 20)
        for vakan in vakans:
            try:
                #lnk_vak = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "g-user-content")))
                #wait = WebDriverWait(vakan, 20)
                #lnk_vak = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "g-user-content")))
                #lnk_vak=vakan.find_element_by_class_name("g-user-content")
                #lnk = vakan.find_element_by_class_name("loko-link HH-LinkModifier")
                lnk = vakan.attrs['href']
                #browser.switch_to_window(browser.window_handles[1])
                browser1.get(lnk)
                soup1 = BeautifulSoup(browser1.page_source)
                descrs = soup1.find_all("div", class_="vacancy-branded-user-content")
                if len(descrs)==0:
                    descrs = soup1.find_all("div", class_="g-user-content")
                qvak_name = soup1.find("h1", class_="header").text
                vakans = soup1.find("div", class_="vacancy-company-wrapper")
                if vakans == None:
                    vakans = soup1.find("p", class_="vacancy-company-wrapper")

                vEmploy_link = ""
                try:
                    vEmploy_link = vakans.find("img", class_="vacancy-company-logo__image").attrs.get("src")
                except:
                    pass
                if vEmploy_link=="":
                    try:
                        vEmploy_link = vakans.find("img",{"class": "vacancy-company-logo__image"}).attrs.get("src")
                    except:
                        pass


                vEmploy_name = ""
                try:
                    vEmploy_name = vakans.find("a", class_="vacancy-company-name").text
                except:
                    pass

                vAddr=""
                try:
                    vAddr = vakans.find("span",{"data-qa" : "vacancy-view-raw-address"}).text
                except:
                    pass
                if vAddr=="":
                    try:
                        vAddr = vakans.find("meta",{"itemprop": "addressRegion"}).attrs.get("content")
                        ch = False
                        for adr in vakans.findAll("span", {"class": "metro-station"}):
                            if not ch:
                                vAddr += "\nМетро:\n"
                                ch = True
                            vAddr += adr.text+"\n"
                    except:
                        pass

                vpsdata=""
                try:
                    vpsdata = vakans.find("meta", {"itemprop": "validThrough"}).attrs.get("content")
                except:
                    pass

                print(qvak_name)
                qvak_sal = soup1.find("p", class_="vacancy-salary").text
                qvak_id = 0
                for desc in descrs:
                    vps = desc.find_all("p")
                    for vp in vps:
                        qvak_id +=1
                        qvak_text=vp.text
                        lis = desc.find_all("li")
                        for li in lis:
                            if li.text not in qvak_text:
                                qvak_text += li.text+"\n"
                        try:
                            cur.execute(sql, [vKeyWord,qvak_name, qvak_sal, qvak_id, qvak_text, lnk, vEmploy_link, vEmploy_name, vAddr, vpsdata])
                        except:
                            rg = '[^A-Za-z0-9А-Яа-я\s]+'
                            qvak_name = re.sub(rg, '*', qvak_name)
                            qvak_text = re.sub(rg, '*', qvak_text)
                            cur.execute(sql, [vKeyWord, qvak_name, qvak_sal, qvak_id, qvak_text, lnk, vEmploy_link, vEmploy_name, vAddr, vpsdata])
                        con.commit()
            except Exception as e:
                print ("Error: %s.\n" % str(e), lnk)
                print(traceback.format_exc())
        con.close
        #browser1.quit()
    except Exception as e:
        print(e)

def do_hh(KeyWord):
    nPage = 0
    StoryFile = "pages.cfg"
    brw = webdriver.Chrome('C:\\Users\\17703170\\ChromeDriver\\chromedriver.exe')
    brw.get('https://hh.ru/search/vacancy?area=1&st=searchVacancy&text='+KeyWord)
    brw1 = webdriver.Firefox('C:\\Users\\17703170\\0')
    pages = brw.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[7]/div/span[*]/a")
    for pg in pages:
        pages_clicks = pg.text;
    try:
        npages = int(pg.text)
    except Exception as e:
        print(e)
        npages = 0

    try:
        f = open(StoryFile, "r")
        sPages = f.read(1)
        startPage = 0
        if sPages!= "":
            startPage = int(sPages)
            #lnk_vak = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='bloko-button HH-Pager-Control'][@data-page='17'][@data-qa='pager-page']")))
            brw.get("https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text="+KeyWord+"&page="+startPage)
            lnk_vak.click()
        nPage = startPage+nPage
        f.close()
    except Exception as e:
        print(e)

    while nPage < npages:
        hh_ru(brw, brw1, KeyWord)
        nPage += 1
        wait = WebDriverWait(brw,50)
        try:
            f = open(StoryFile, "w")
            f.write(str(nPage-1))
            f.close()
            #lnk_vak = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[7]/div/span[*]/span["+str(nPage)+"]/a")))
            #lnk_vak.click()
            brw.get("https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text="+KeyWord+"&page=" + str(nPage))
        except TimeoutException as e2:
            print("")
    brw.quit()
    brw1.quit()


do_hh("python")

