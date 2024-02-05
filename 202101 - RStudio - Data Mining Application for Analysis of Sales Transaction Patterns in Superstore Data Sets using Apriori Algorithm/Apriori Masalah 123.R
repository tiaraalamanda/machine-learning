setwd("D:/UNPAR/Semester 3/Komputasi Statistika A/Project")

## Kode Jawaban Rumusan Masalah
library(arules)
library(arulesViz)
sstransaksi <- read.transactions("D:/Semester 3/Komputasi Statistika A/Project/Superstore Data.csv", rm.duplicates = TRUE, sep = ",", format = "single", cols=c(1,2))
itemFrequencyPlot(sstransaksi,type="absolute") #terlihat kategori barang yg paling sedikit dibeli adalah Copiers
itemFrequencyPlot(sstransaksi,topN=20,type="absolute") #diurutkan top 20 kategori barang, walaupun kategori brg hanya ada 18
itemFrequencyPlot(sstransaksi,topN=10,type="absolute") #diurutkan top 10 kategori barang, paling tinggi (kiri), ke kanan (plg rendah)

frequentItems <- eclat (sstransaksi, parameter = list(supp = 0.08))
inspect(frequentItems)
itemFrequency(sstransaksi) #persentase jmlh transaksi tiap kategori dari semua transaksi
#Binder adalah kategori barang yang paling laku, dengan frekuensi transaksi: 26.27% dari seluruh 9994 transaksi
#Copiers adalah kategori barang yang paling kurang laku, dengan frekuensi transaksi: 1.36% dari seluruh 9994 transaksi

rules <- apriori(sstransaksi, parameter = list(supp = 0.001, conf = 0.08))
inspect(rules)
rulessort<- sort(rules, decreasing=TRUE)
inspect(rulessort) #1273 rules yg saling berhubungan krn apriori, akan ditampilkan di console

rules_conf <- sort (rules, by="confidence", decreasing=TRUE) #urutan rules yang dilihat berdasarkan confidence dari paling tinggi
inspect(head(rules_conf))
rules_supp <- sort (rules, by="support", decreasing=TRUE) #urutan rules yang dilihat berdasarkan support dari paling tinggi
inspect(head(rules_supp))

#Item di target, yaitu labels
rules_pilihanlhs<-apriori(data=sstransaksi, parameter=list(supp=0.001,conf = 0.08), 
                          appearance = list(default="rhs",lhs="Labels"),
                          control = list(verbose=F))
rules<-sort(rules_pilihanlhs, decreasing=TRUE,by="confidence")
inspect(rules_pilihanlhs) #Milih agar yg muncul di console adalah semua Labels yg sdh di sort di lhs

rules_pilihanrhs<-apriori(data=sstransaksi, parameter=list(supp=0.001,conf = 0.08), 
               appearance = list(default="lhs",rhs="Labels"),
               control = list(verbose=F))
rules<-sort(rules_pilihanrhs, decreasing=TRUE,by="confidence")
inspect(rules_pilihanrhs) #Milih agar yg muncul di console adalah semua Labels yg sdh di sort di rhs

## Jawaban Rumusan Masalah No 1
#Gambar
library(arulesViz)
plot(rules,method="graph",interactive=TRUE,shading=NA)
