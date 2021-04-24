### flask-api-mysql
# Config Dosyası
- [DB], [LOGGING] ve [API] kısımlarında parametreler tanımlanmıştır.

# Endpointler

##  Select
- __/select__ endpointi sadece **GET** metodunu kabul eder.
- Gönderilen tablo ismini veritabanından çeker.
- Veritabanında kullanılacak tablo ismi aşağıdaki gibi belirtilmelidir :
```
 /select?=table_name=*test*
```
- Aşağıdaki parametreler kullanarak sorgu yapılabilinir.
```
 "firstname", "lastname", "email", "id" 
```

##  Insert
- __/insert__ endpointi sadece **POST** ve **PUT** metodlarını kabul eder.
- Tablo ismi belirtmek zorunludur.
- **POST** metodu aşağıdaki gibi kullanılabilinir, JSON formatında body alamaz :
```
/insert?table_name=TEST&firstname=ISIM&lastname=SOYISIM&email=EMAIL@EMAIL.COM
```
- **PUT** metodu sadece JSON body formatını kabul eder.
```
{
  "firstname" : "isim"
  "lastname" : "soyisim"
  "email" : "email@email.com"
}
```

## Delete
- __/delete__ endpointi sadece **DELETE** metodunu kabul eder.
- Tablo ismi belirtmek zorunludur.
- Aşağıdaki örnekteki gibi verilen email parametresine göre tablodan veri silinebilir:
```
/delete?table_name=TEST&email=EMAIL@EMAIL.COM
```
- Aşağıdaki parametrelerle sorgular yapılabilinir :
```
firstname,
lastname,
email,
firstname & lastname,
firstname & email,
lastname & email
```

## Update
- __/update__ endpointi sadece **POST** metodunun kabul eder.
- Tablo ismi belirtmek zorunludur.
- Sadece **id** verilerek veya sadece **email** verilerek **UPDATE** işlemi yapılabilinir.
