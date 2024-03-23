from .models import BrickProduct

def generate_product_code():
    last_product = BrickProduct.objects.order_by('-id').first()
    if last_product and last_product.product_code:
        last_code = last_product.product_code
        last_num = int(last_code.split('-')[1])
        new_num = last_num + 1
        product_code = f'HB-{str(new_num).zfill(4)}'
    else:
        product_code = 'HB-0001'
    return product_code