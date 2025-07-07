from django.db import models
from django.contrib.auth import get_user_model
class DrugCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class DrugUnits(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Drug(models.Model):
    name_ar = models.CharField(max_length=255, verbose_name="اسم الصنف العربي")
    name_en = models.CharField(max_length=255, verbose_name="اسم الصنف الإنجليزي", null=True)

    agent = models.CharField(max_length=255, verbose_name="الوكيل", blank=True, null=True)
    show_agent = models.BooleanField(default=True, verbose_name="عرض الوكيل")

    manufacturer = models.CharField(max_length=255, verbose_name="الشركة المنتجة", blank=True, null=True)
    show_manufacturer = models.BooleanField(default=True, verbose_name="عرض الشركة المنتجة")

    country_of_origin = models.CharField(max_length=255, verbose_name="بلد التصنيع", blank=True, null=True)
    show_country_of_origin = models.BooleanField(default=True, verbose_name="عرض بلد التصنيع")

    scientific_name = models.CharField(max_length=255, verbose_name="الاسم العلمي", blank=True, null=True)
    show_scientific_name = models.BooleanField(default=True, verbose_name="عرض الاسم العلمي")
    category = models.ForeignKey(DrugCategory, on_delete=models.SET_NULL, null=True, related_name='drugs',verbose_name="الفئة")
    unit = models.ForeignKey(DrugUnits, on_delete=models.SET_NULL, null=True, related_name='drugs') 

    usage = models.TextField(verbose_name="دواعي الاستعمال", blank=True, null=True)
    show_usage = models.BooleanField(default=True, verbose_name="عرض دواعي الاستعمال")
    description = models.TextField(verbose_name="الوصف", blank=True, null=True)
    show_description = models.BooleanField(default=True, verbose_name="عرض الوصف")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر", blank=True, null=True)
    show_price = models.BooleanField(default=True, verbose_name="عرض السعر")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الانتهاء")
    show_expiry_date = models.BooleanField(default=True, verbose_name=  "عرض تاريخ الانتهاء")
    image = models.ImageField(upload_to='drug_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_ar



User = get_user_model()

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.drug.name_ar} x {self.quantity}"

    def total_price(self):
        return self.quantity * self.price_at_order


class Offer(models.Model):
  title = models.CharField(max_length=255, verbose_name="العنوان")
  description = models.TextField(verbose_name="الوصف", blank=True, null=True)
  image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
        return self.title