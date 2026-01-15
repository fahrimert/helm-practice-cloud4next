# Helm Pratiği ve Öğrenimi Projesi

![alt text](assets/image-16.png)

Bu projede Helm pratiği yapmak amacıyla **NGINX** chart’ı seçilmiştir (nginx / redis seçenekleri arasından nginx tercih edilmiştir).

## Ortam Kurulumu
Vagrant kullanılarak bir sanal makine oluşturulmuş, ardından Ansible ile bu sanal makine üzerine aşağıdaki bileşenler kurulmuştur:

- k3s
- Helm
- Gerekli sistem paketleri

Kurulum tamamlandıktan sonra sanal makineye SSH ile bağlantı sağlanmıştır.

## Helm Repository Ekleme
Bitnami Helm repository’si Helm’e eklenmiştir:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami


```
## Chart İndirme ve Hazırlık
NGINX chart’ı, values.yaml dosyası üzerinde değişiklik yapılabilmesi ve chart yapısının incelenebilmesi amacıyla lokal ortama indirilmiş ve extract edilmiştir:

```bash
helm pull bitnami/nginx --untar
```
## Uygulamanın Yüklenmesi

İndirilen yerel klasör (./nginx) kaynak gösterilerek kurulum yapılmıştır. Bu aşamada varsayılan ayarlar kullanılmıştır:

```bash
helm install my-nginx ./nginx --namespace default
```

## Doğrulama

Kurulumun durumu helm list komutu ile kontrol edilmiştir:

```bash
root@mert-k3slab-server:/home/vagrant/helm-practice/nginx# helm list
NAME        NAMESPACE   REVISION    UPDATED                                 STATUS      CHART           APP VERSION
my-nginx    default     2           2026-01-14 15:41:16.590279955 +0000 UTC deployed    nginx-22.4.3    1.29.4
```


## Soru: Helm status komutu çıktısındaki "Notes" bölümü ne işe yarar?

http://suyog942.medium.com/demystifying-helm-a-practical-guide-to-notes-txt-9acdb111fb6a 
bu makaleyi aldım baz olarak helm status notes bölümü  chartName/templates/NOTES.txt dosyasındaki bilgileri yazıyor genel olarak benim nginx deploymentimda chart name , chart versiyon ve sadece app versiyonum yazıyordu benim helm status notes kısmım dolayısıyla aşşağıdaki gibi.

## Bu Projedeki Çıktı
Kullandığım bitnami/nginx chart'ının bu sürümünde NOTES.txt çıktısı şu şekildedir:
```bash
NOTES:
CHART NAME: nginx
CHART VERSION: 22.4.3
APP VERSION: 1.29.4 
```

## Yapılandırma ve "Values.yaml"
![alt text](assets/image-17.png)

Öncesinde values.yaml dosyamda replica sayım 1 ve resources kısmım tamamen default olarak :
```bash
    Limits:
      cpu:                150m
      ephemeral-storage:  2Gi
      memory:             192Mi
    Requests:
      cpu:                100m
      ephemeral-storage:  50Mi
      memory:             128Mi
```

değerlerine sahipti kubectl describe pod komudu ile bunları gördüm. 

![alt text](assets/image-8.png)

Sonrasında ise values.yaml dosyamı değiştirerek bu değerleri istenen değerler gibi güncelledim.

![alt text](assets/image-11.png)

![alt text](assets/image-6.png)

Ve şu sonuçları gördüm.Bu sonuçlar ile başarılı bir şekilde güncelleme işlemlerimi yapmış oldum 
Güncelleme işlemlerini yaparken şu komudu kullandım:
```bash
 helm upgrade my-nginx ./nginx 
```
![alt text](assets/image-10.png)

![alt text](assets/image-12.png)

## Kendi Chart'ını Oluşturma (Deep Dive)

![alt text](assets/image-18.png)

Repomda bulunan hello-app klasörünün altında python flask ile kurmuş olduğum istek attığım zaman "Hello World! Kubernetes ve Helm çalışıyor" responsesini veren uygulama ile Dockerfile sini yazdım

Daha sonrasında helm ile templatesini kurmadan öncesinde:
![alt text](assets/image-18.png)

Yeni bir ansible dosyası kurmam gerekti. Bu sayede helm chart ile kullanabileceğim hello-app uygulamamın imagesini Vm`in içerisine koymuş oldum.

Daha sonrasında komudu ile templatemi oluşturdum.

```bash
helm create hello-app 
```

Helm lint komudunun çıktısı:
![alt text](assets/image-13.png)

```bash
helm install hello-world-app ./hello-app
```
bu komut ile uygulamamı ayağa kaldırdım. 

![alt text](assets/image-14.png)

![alt text](assets/image-15.png)


##  Release Yönetimi ve Geri Dönüş (Rollback)
Nginxin bozulması için nginx chartındaki values.yaml dosyasındaki image kısmındaki nginx yazısı yerine nginxx yaparak test ettim.

![alt text](assets/image-1.png)

![alt text](assets/image-2.png)

Daha sonrasında şu komut ile release yönetimi için nginximin releaselerine baktım:

```bash
helm history my-nginx
```

![alt text](assets/image-3.png)

Daha sonrasında şu komut ile tam bir önceki versiyona döndüm spesifik olarak bir versiyon belirtmeden 
```bash
helm rollback my-nginx 1
```

![alt text](assets/image-4.png)

ve sonrasında ise nginx podlarım yeniden çalışmaya devam etti.


