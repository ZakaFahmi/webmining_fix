#!/usr/bin/env python
# coding: utf-8

# nama: M. Salisianto Fahmi Zaka <br>
# nim : 190411100027 <br>
# matakuliah : ppw kelas A

# ## Install & Import Library
# Jika anda ingin menjalankan notebook secara offline seperti Jupyter Notebook, pastikan perangkat anda sudah terinstall library yang dibutuhkan. Jika anda ingin menjalankan notebook secara online seperti Google Colaboratory, pastikan notebook tersebut sudah terinstall library yang dibutuhkan. Library yang dibutuhkan dalam proyek ini, yaitu:
# - Scrapy
# - OS
# - Regex
# - Pandas
# - Matplotlib

# In[1]:


get_ipython().system('pip install Sastrawi')
get_ipython().system('pip install Scrapy')


# In[2]:


# Import Library
import os
import regex as re
import pandas as pd
import nltk
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# Install NLTK Corpus
nltk.download('stopwords')
nltk.download('punkt')


# # Crawling Data

# ## Create Scrapy Project
# 
# Pada bagian ini digunakan untuk membuat proyek library Scrapy dan memindah posisi direktori. Proyek library Scrapy diberi nama crawlproject. Posisi direktori dipindah ke crawlproject/crawlproject/spiders

# In[3]:


# Membuat proyek library Scrapy
get_ipython().system('scrapy startproject crawlproject')


# In[4]:


# Melihat posisi direktori saat ini
os.getcwd()


# In[5]:


# Mengubah posisi direktori saat ini ke crawlproject/crawlproject/spiders
# Fungsinya agar bisa menjalankan file proyek library Scrapy
os.chdir('crawlproject/crawlproject/spiders')
os.getcwd()


# ## Crawling Link PTA
# 
# Pada bagian ini digunakan untuk membuat dan menjalankan program python. Program tersebut digunakan untuk melakukan _crawling_ 60 link . Untuk melakukan _crawling_ menggunakan library scrapy.

# In[6]:


get_ipython().run_cell_magic('writefile', '-a link.py', '# Membuat file link.py\n# File link.py digunakan untuk crawling link tugas akhir\nimport scrapy\n\nclass QuotesSpider(scrapy.Spider):\n    name = "quotes"\n\n    def start_requests(self):\n        start_urls = [\'https://pta.trunojoyo.ac.id/c_search/byprod/10/1\']\n        for i in range (2,13):\n            tambah = \'https://pta.trunojoyo.ac.id/c_search/byprod/10/\'+ str(i)\n            start_urls.append(tambah)\n        for url in start_urls:\n            yield scrapy.Request(url=url, callback=self.parse)\n\n    def parse(self, response):\n        for i in range(1, 6):\n            yield {\n                \'link\':response.css(\'#content_journal > ul > li:nth-child(\' +str(i)+ \') > div:nth-child(3) > a::attr(href)\').extract()\n            }\n')


# In[7]:


# Menjalankan file link.py untuk melakukan proses crawling link tugas akhir
# Hasil akan disimpan dalam file link.csv
# File link.csv digunakan untuk melakukan crawling detail tugas akhir
get_ipython().system('scrapy runspider link.py -o link.csv')


# ## Crawling Detail PTA
# 
# Pada bagian ini digunakan untuk membuat dan menjalankan program python. Program tersebut digunakan untuk melakukan crawling 60n. Untuk melakukan crawling menggunakan library scrapy.

# In[8]:


get_ipython().run_cell_magic('writefile', '-a detail.py', '# Membuat file detail.py\n# File detail.py digunakan untuk crawling detail tugas akhir\nimport scrapy\nimport pandas as pd\n\nclass QuotesSpider(scrapy.Spider):\n    name = "quotes"\n\n    def start_requests(self):\n        dataCSV = pd.read_csv(\'link.csv\')\n        indexData = dataCSV.iloc[:, [0]].values\n        arrayData = []\n        for i in indexData:\n            ambil = i[0]\n            arrayData.append(ambil)\n        for url in arrayData:\n            yield scrapy.Request(url=url, callback=self.parse)\n\n    def parse(self, response):\n        yield {\n            \'judul\': response.css(\'#content_journal > ul > li > div:nth-child(2) > a::text\').extract(),\n            \'penulis\': response.css(\'#content_journal > ul > li > div:nth-child(2) > div:nth-child(2) > span::text\').extract(),\n            \'pembimbing_1\': response.css(\'#content_journal > ul > li > div:nth-child(2) > div:nth-child(3) > span::text\').extract(),\n            \'pembimbing_2\': response.css(\'#content_journal > ul > li > div:nth-child(2) > div:nth-child(4) > span::text\').extract(),\n            \'abstrak\': response.css(\'#content_journal > ul > li > div:nth-child(4) > div:nth-child(2) > p::text\').extract()\n        }\n')


# In[9]:


# Menjalankan file detail.py untuk melakukan proses crawling detail tugas akhir
# Hasil akan disimpan dalam file detail.csv
# File detail.csv digunakan sebagai dataset utama yang diolah dalam proyek ini
get_ipython().system('scrapy runspider detail.py -o detail.csv')

