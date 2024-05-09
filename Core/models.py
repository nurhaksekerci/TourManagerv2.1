from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
class Sirket(models.Model):
    STATU_CHOICES = (
        ('demo', 'Demo'),
        ('basic', 'Basic'),
        ('team', 'Team'),
        ('professional', 'Professional'),
    )
    name = models.CharField(verbose_name="Adı", max_length=155)
    start = models.DateField(verbose_name="Başlama Tarihi")
    finish = models.DateField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(verbose_name="Aktif mi?")
    statu = models.CharField(max_length=20, choices=STATU_CHOICES, verbose_name="Statü", default="demo")
    created_at = models.DateField(verbose_name="Kurulma Tarihi", auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.name

class Personel(models.Model):
    JOB_CHOICES = (
        ('Satış Personeli', 'Satış Personeli'),
        ('Operasyon Şefi', 'Operasyon Şefi'),
        ('Yönetim', 'Yönetim'),
        ('Muhasebe', 'Muhasebe'),
        ('Sistem Geliştiricisi', 'Sistem Geliştiricisi'),
    )
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name='personel')
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Aktif mi?", default=True)
    phone = models.CharField(verbose_name="Telefon", max_length=50, blank=True, null=True)
    job = models.CharField(max_length=20, choices=JOB_CHOICES, verbose_name="Görevi", default="Satış Personeli")
    created_at = models.DateField(verbose_name="Kurulma Tarihi", auto_now_add=True, blank=True, null=True)
    dark_mode = models.BooleanField(verbose_name="Dark Mode", default=False)


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name.upper()
    
class Tour(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Güzergah", max_length=155)
    sellcar = models.DecimalField(verbose_name="Araç Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sellminivan = models.DecimalField(verbose_name="Minivan Satış", max_digits=10, decimal_places=2, blank=True, null=True)
    sellminibus = models.DecimalField(verbose_name="Minibüs Satış", max_digits=10, decimal_places=2, blank=True, null=True)
    sellmidibus = models.DecimalField(verbose_name="Midibüs Satış", max_digits=10, decimal_places=2, blank=True, null=True)
    sellbus = models.DecimalField(verbose_name="Otobüs Satış", max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.route

class Transfer(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Güzergah", max_length=155)
    sellcar = models.DecimalField(verbose_name="Binek Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sellminivan = models.DecimalField(verbose_name="Minivan Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sellminibus = models.DecimalField(verbose_name="Minibüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sellmidibus = models.DecimalField(verbose_name="Midibüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sellbus = models.DecimalField(verbose_name="Otobüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.route

class Vehicle(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    vehicle = models.CharField(verbose_name="Araçlar", max_length=155)
    capacity = models.PositiveIntegerField(verbose_name="Kapasite")

    def __str__(self):
        return self.vehicle

class Guide(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=155)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    doc_no = models.CharField(verbose_name="Rehber No", max_length=155, blank=True, null=True)
    phone = models.CharField(verbose_name="Telefon No", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155, blank=True, null=True)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.city} - {self.name}"

class Hotel(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155, blank=True, null=True)
    one_person = models.DecimalField(verbose_name="Tek Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    two_person = models.DecimalField(verbose_name="İki Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    tree_person = models.DecimalField(verbose_name="Üç Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    finish = models.DateField(verbose_name="Fiyat Geçerlilik Tarihi", blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.name} - {self.city}"

class Activity(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )

    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)

    def __str__(self):
        return f"{self.city} - {self.name}"

class Museum(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )

    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    contact = models.CharField(verbose_name="İletişim", max_length=155)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.city} - {self.name}"

class Supplier(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    contact = models.CharField(verbose_name="İletişim", max_length=155)

    def __str__(self):
        return f"{self.name}"

class Activitysupplier(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    contact = models.CharField(verbose_name="İletişim", max_length=155)

    def __str__(self):
        return f"{self.name}"

class Cost(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name="Tedarikçi", on_delete=models.SET_NULL, blank=True, null=True)
    tour = models.ForeignKey(Tour, verbose_name="Tur", on_delete=models.SET_NULL, blank=True, null=True)
    transfer = models.ForeignKey(Transfer, verbose_name="Transfer", on_delete=models.SET_NULL, blank=True, null=True)
    car = models.DecimalField(verbose_name="Maliyet Binek", max_digits=10, decimal_places=2, blank=True, null=True)
    minivan = models.DecimalField(verbose_name="Maliyet Minivan", max_digits=10, decimal_places=2, blank=True, null=True)
    minibus = models.DecimalField(verbose_name="Maliyet Minibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    midibus = models.DecimalField(verbose_name="Maliyet Midibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    bus = models.DecimalField(verbose_name="Maliyet Otobüs", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        if self.tour != None:
            return f"{self.tour} {self.supplier.name}"
        else:
            return f"{self.transfer} {self.supplier.name}"

class Activitycost(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Activitysupplier, verbose_name="Aktivite Tedarikçisi", on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(Activity, verbose_name="Activite", on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.supplier} - {self.activity}"

class Buyercompany(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name="Adı", max_length=100)
    short_name = models.CharField(verbose_name="Kısa adı", max_length=5, unique=True)
    contact = models.CharField(verbose_name="İletişim", max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name


class UserActivityLog(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket (公司)", on_delete=models.CASCADE, blank=True, null=True)
    staff = models.ForeignKey(Personel, verbose_name="Personel", on_delete=models.SET_NULL, blank=True, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.action} - {self.timestamp}"
    





class Operation(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('Pesin', 'Peşin'),
        ('Taksitli', 'Taksitli'),
        ('Parcalı', 'Parçalı'),
    )
    PAYMENT_CHANNEL_CHOICES = (
        ('Havale', 'Havale'),
        ('Xctrip', 'Xctrip'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)


    selling_staff = models.ForeignKey(Personel, verbose_name="Satan Personel", related_name="Satan", on_delete=models.SET_NULL, blank=True, null=True)
    follow_staff = models.ForeignKey(Personel, verbose_name="Takip Eden Personel", related_name="Takip", on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Güncelleme Tarihi", auto_now=True, auto_now_add=False)
    
    buyer_company = models.ForeignKey(Buyercompany, verbose_name="Alıcı Firma", related_name="Alıcı", on_delete=models.SET_NULL, blank=True, null=True)
    ticket = models.CharField(verbose_name="Tur Etiketi", unique=True, max_length=50, blank=True, null=True)
    
    start = models.DateField(verbose_name="Başlama Tarihi")
    finish = models.DateField(verbose_name="Bitiş Tarihi")
    
    passenger_info = models.TextField(verbose_name="Yolcu Bilgileri")
    number_passengers = models.PositiveIntegerField(verbose_name="Yolcu Sayısı", default=1)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES,  blank=True, null=True, verbose_name="Ödeme Türü")
    payment_channel = models.CharField(max_length=20, choices=PAYMENT_CHANNEL_CHOICES,  blank=True, null=True, verbose_name="Ödeme Kanalı")
    remaining_payment = models.DecimalField(verbose_name="Kalan Ödeme", max_digits=10, decimal_places=2, default=0)
    
    tl_sales_price = models.DecimalField(verbose_name="TL Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    usd_sales_price = models.DecimalField(verbose_name="USD Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    eur_sales_price = models.DecimalField(verbose_name="EUR Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    rbm_sales_price = models.DecimalField(verbose_name="RBM Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    
    tl_cost_price = models.DecimalField(verbose_name="TL Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    usd_cost_price = models.DecimalField(verbose_name="USD Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    eur_cost_price = models.DecimalField(verbose_name="EUR Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    rbm_cost_price = models.DecimalField(verbose_name="RBM Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.ticket}"



class Operationday(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operasyon", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Tarih")

    def __str__(self):
        return self.date.strftime("%d-%m-%Y")
    

class Operationitem(models.Model):
    OPERATIONSTYPE_CHOICES = (
        ('Transfer', 'Transfer'),
        ('Tur', 'Tur'),
        ('TurTransfer', 'Tur + Transfer'),
        ('TransferTur', 'Transfer + Tur'),
        ('Arac', 'Araç'),
        ('Aktivite', 'Aktivite'),
        ('Muze', 'Müze'),
        ('Otel', 'Otel'),
        ('Rehber', 'Rehber'),
        ('Aracli Rehber', 'Araçlı Rehber'),
        ('Serbest Zaman', 'Serbest Zaman'),
    )
    ROOMTYPE_CHOICES = (
        ('Tek', 'Tek'),
        ('Cift', 'Çift'),
        ('Uc', 'Üç'),
    )
    TRUE_FALSE_CHOICES = (
        ('Evet', 'Evet'),
        ('Hayır', 'Hayır'),
    )
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)
    day = models.ForeignKey(Operationday, verbose_name="Gün", on_delete=models.CASCADE)

    operation_type = models.CharField(max_length=20, choices=OPERATIONSTYPE_CHOICES, verbose_name="İşlem Türü")
    pick_time = models.TimeField(blank=True, null=True, verbose_name="Alış Saati")
    release_time = models.TimeField(blank=True, null=True, verbose_name="Bırakış Saati")
    release_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Bırakış Yeri")
    pick_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alış Yeri")


    tour = models.ForeignKey(Tour, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Tur")
    transfer = models.ForeignKey(Transfer, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Transfer")
    vehicle = models.ForeignKey(Vehicle, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Araç")
    supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Araç Tedarikçi")
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Araç Ücreti")
    vehicle_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Araç Para Birimi", default="USD")
    cost = models.ForeignKey(Cost, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Araç Maaliyet")

    hotel = models.ForeignKey(Hotel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Otel")
    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES, blank=True, null=True, verbose_name="Oda Türü")
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Otel Ücreti")
    hotel_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Otel Para Birimi", default="USD")
    hotel_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Otel Ödemesi Bizde", default="Hayır")

    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Aktivite")
    activity_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Aktivite Ücreti")
    activity_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Aktivite Para Birimi", default="USD")
    activity_supplier = models.ForeignKey(Activitysupplier, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Aktivite Tedarikçi")
    activity_cost = models.ForeignKey(Activitycost, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Aktivite Maliyet")
    activity_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Activite Ödemesi Bizde", default="Hayır")

    new_museum = models.ManyToManyField(Museum, blank=True, verbose_name="Müzeler", related_name="new_operation_items")
    museum_person = models.IntegerField(verbose_name="Müze Kişi Sayısı", default=0)
    museum_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Müze Ücreti")
    museum_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Müze Para Birimi", default="USD")
    museum_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Müze Ödemesi Bizde", default="Hayır")

    driver = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şoför")
    driver_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şoför Telefon")
    plaka = models.CharField(max_length=255, blank=True, null=True, verbose_name="Plaka")
    guide = models.ForeignKey(Guide, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Rehber")
    guide_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Rehber Ücreti")
    guide_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Rehber Para Birimi", default="USD")
    other_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Diğer Ücretler")
    other_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Diğer Ücretler Para Birimi", default="USD")
    
    
    tl_cost_price = models.DecimalField(verbose_name="TL Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    usd_cost_price = models.DecimalField(verbose_name="USD Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    eur_cost_price = models.DecimalField(verbose_name="EUR Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    rmb_cost_price = models.DecimalField(verbose_name="RMB Maliyet Fiyatı", max_digits=10, decimal_places=2, default=0)
    
    description = models.TextField(verbose_name="Tur Detayı", blank=True, null=True)

    def __str__(self):
        return f"{self.day} - {self.operation_type}"
    
    

    


class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Açık'),
        ('in_progress', 'İşlemde'),
        ('closed', 'Kapalı'),
    )
    
    TITLE_CHOICES = (
        ('login_issue', 'Giriş Sorunu'),
        ('payment_issue', 'Ödeme Sorunu'),
        ('bug_report', 'Hata Bildirimi'),
        ('account_info', 'Hesap Bilgisi Sorgulama'),
        ('suggestion', 'Öneri'),
        ('training', 'Eğitim'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    user = models.ForeignKey(Personel, verbose_name="Kaydı Açan", on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, choices=TITLE_CHOICES, default='login_issue', verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Durum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Zamanı")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Zamanı")

    def __str__(self):
        return f"{self.get_title_display()} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Destek Kaydı"
        verbose_name_plural = "Destek Kayıtları"




class Notification(models.Model):
    JOB_CHOICES = (
        ('Herkes', 'Herkes'),
        ('Satış Personeli', 'Satış Personeli'),
        ('Operasyon Şefi', 'Operasyon Şefi'),
        ('Yönetim', 'Yönetim'),
        ('Muhasebe', 'Muhasebe'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(Personel, related_name='sent_notifications', on_delete=models.CASCADE)
    recipients_group = models.CharField(max_length=20, choices=JOB_CHOICES, verbose_name="Mesaj Grupları", default="Herkes")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to multiple recipients - {self.title}"

class NotificationReceipt(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='receipts')
    recipient = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name='received_notifications')
    read_at = models.DateTimeField(null=True, blank=True)  # Eğer null ise, henüz okunmamıştır.

    class Meta:
        unique_together = ('notification', 'recipient')  # Her bir personel için bir bildirimi bir kere kaydetmek.

    def __str__(self):
        read_status = 'Okundu' if self.read_at else 'Okunmadı'
        return f"{self.recipient.user.username} - {read_status}"
    


class OperationTemplate(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Şablon Adı", unique=True, max_length=50, blank=True, null=True)
    buyer_company = models.ForeignKey(Buyercompany, verbose_name="Alıcı Firma", on_delete=models.SET_NULL, blank=True, null=True)
    day_numbers = models.IntegerField(verbose_name="Gün Sayısı")
    tl_sales_price = models.DecimalField(verbose_name="TL Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    usd_sales_price = models.DecimalField(verbose_name="USD Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    eur_sales_price = models.DecimalField(verbose_name="EUR Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    rbm_sales_price = models.DecimalField(verbose_name="RBM Satış Fiyatı", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"
    
class OperationdayTemplate(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)
    operation = models.ForeignKey(OperationTemplate, verbose_name="Operasyon Şablonu", on_delete=models.CASCADE)
    day_number = models.IntegerField(verbose_name="Gün Numarası", blank=True, null=True)

    def __str__(self):
        return f"{self.day_number} - {self.operation.name}"
    

class OperationitemTemplate(models.Model):
    OPERATIONSTYPE_CHOICES = (
        ('Transfer', 'Transfer'),
        ('Tur', 'Tur'),
        ('TurTransfer', 'Tur + Transfer'),
        ('TransferTur', 'Transfer + Tur'),
        ('Arac', 'Araç'),
        ('Aktivite', 'Aktivite'),
        ('Muze', 'Müze'),
        ('Otel', 'Otel'),
        ('Rehber', 'Rehber'),
        ('Aracli Rehber', 'Araçlı Rehber'),
        ('Serbest Zaman', 'Serbest Zaman'),
    )
    ROOMTYPE_CHOICES = (
        ('Tek', 'Tek'),
        ('Cift', 'Çift'),
        ('Uc', 'Üç'),
    )
    TRUE_FALSE_CHOICES = (
        ('Evet', 'Evet'),
        ('Hayır', 'Hayır'),
    )
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE)
    operation = models.ForeignKey(OperationTemplate, verbose_name="Operasyon Şablonu", on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=20, choices=OPERATIONSTYPE_CHOICES, verbose_name="İşlem Türü")
    pick_time = models.TimeField(blank=True, null=True, verbose_name="Alış Saati")
    release_time = models.TimeField(blank=True, null=True, verbose_name="Bırakış Saati")
    day = models.ForeignKey(OperationdayTemplate, verbose_name="Operasyonday Şablonu", on_delete=models.CASCADE,blank=True, null=True)

    tour = models.ForeignKey(Tour, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Tur")
    transfer = models.ForeignKey(Transfer, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Transfer")
    vehicle = models.ForeignKey(Vehicle, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Araç")

    hotel = models.ForeignKey(Hotel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Otel")
    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES, blank=True, null=True, verbose_name="Oda Türü")
    hotel_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Otel Ödemesi Bizde", default="Hayır")

    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Aktivite")
    activity_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Activite Ödemesi Bizde", default="Hayır")

    new_museum = models.ManyToManyField(Museum, blank=True, verbose_name="Müzeler")
    museum_payment = models.CharField(max_length=20, choices=TRUE_FALSE_CHOICES, verbose_name="Müze Ödemesi Bizde", default="Hayır")

    description = models.TextField(verbose_name="Tur Detayı", blank=True, null=True)

    def __str__(self):
        return f"{self.operation} - {self.operation_type}"