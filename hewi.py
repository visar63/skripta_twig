from io import BytesIO
from urllib import response
import requests
import re
import time
import os
class Hewi:
    def __init__(self):
       self.s =requests.Session()

    def Login(self,email,password):
        print('Login loading...!!')
        response0 = requests.get(url='https://hardlyeverwornit.com/login')
        if response0.status_code == 200 and 'Sign In' in response0.text:
            # print('response0:',response0.headers['set-cookie'])
            self.cookie1 = response0.headers['set-cookie'].split(";")[0].split("=")[1]
            hewi_token = re.search(r'p_security_token" value="(.*?)"', response0.text, re.I | re.S).group(1)
            payload = {
                '_username':email ,
                '_password': password ,
                '_csrf_shop_security_token': hewi_token,
            }  
            headers={
                'cookie':'PHPSESSID={0}'.format(self.cookie1),
            }  
            response = requests.post(url="https://hardlyeverwornit.com/login-check",data=payload,headers=headers)
            # print('response:',response.headers['set-cookie'])
            self.cookie2 = response.headers['set-cookie'].split(";")[0].split("=")[1]
            self.headers0 = {
                'cookie':'PHPSESSID={0}'.format(self.cookie2)
            }
            print(f'{self.cookie2 = }')
            print('Login OK')
            return response

    def Product_ID_(self):
        response1 =requests.get(url = 'https://hardlyeverwornit.com/account/sell/product/create',headers=self.headers0)
        if response1:
            location = response1.history[0].headers['location']
            # print(f'{location = }')
            # cookie = response1.history[0].headers['set-cookie']
            # print(f'{cookie = }')
            self.product_ID = re.search('edit/(.*?)$',str(location),re.I|re.S).group(1)
            # if you has to check sepcifik ID
            # self.product_ID=85271    
            print('NEW Product ID:',self.product_ID)
            self.headers = {
                'cookie': 'PHPSESSID={0}'.format(self.cookie2),
                'origin': 'https://hardlyeverwornit.com',
                'referer': 'https://hardlyeverwornit.com/account/sell/product/edit/{0}'.format(self.product_ID),
                }
            content_product =requests.get(
                url='https://hardlyeverwornit.com/account/sell/product/edit/{0}'.format(self.product_ID),
                headers=self.headers)
            self.general_token = re.search(r'general__token" name="general.*?" value="(.*?)"',content_product.text,re.I|re.S).group(1)
            self.crf_token = re.search(r'csrf&quot;:&quot;(.*?)&quot;',content_product.text,re.I|re.S).group(1)
        else:
            print("Error!")

    def upload_images(self,row):
        try:
            img_headers={
            'cookie': 'PHPSESSID={0}'.format(self.cookie2),
            'origin': 'https://hardlyeverwornit.com',
            'referer': 'https://hardlyeverwornit.com/account/sell/product/edit/{0}'.format(self.product_ID),
            }
            img_len = len(row['images'])
            img_id = None
            all_responses = []
            for i in range(0, img_len):
                img_url = row['images'][i]
                # print(f'img url: {img_url}')
                img_name = img_url.split("/")[-1]
                img = BytesIO(requests.get(img_url, stream=True).raw.read())
                files=[
                ('file',('photo1.jpeg',img,'image/jpeg'))
                ]
                payload={
                '_token': self.crf_token,
                'thumbnail_filter': 'shop_product_thumbnail'}
                response = requests.post(
                    url='https://hardlyeverwornit.com/account/product/{0}/media'.format(self.product_ID), 
                    headers=img_headers, 
                    data=payload, 
                    files=files,
                    )
                if response.ok:
                    img_id = response.json()['id']
                    print("img id: " + str(img_id))
                all_responses.append(img_id)
                # print(all_responses)
            if None in all_responses:
                return False
            print('Images are uploaded')
            return all_responses
        except:
            print('image has error in upload')

    def create_draft_body(self):
        
        self.body ={
            'general[mainTaxon]': '25',
            'general[designer]': '54',
            'general[suggestedDesigner]': '',
            'general[size]': '17',        # vd: me kriju fushen row['size_id']
            'general[sizeOnLabel]': '40', # vd: duhet me rujt fushen row['size'] 
            'general[itemCondition]': 'worn_in_good_condition',
            'general[fabric]': 'cotton',  # material ska nevoj me u mapu
            'general[colour]': 'red',     # vd: duhet me rujt fushen row['color']
            'general[nearestColour]': '3',# vd: me kriju fushen row['color_id']
            'general[description]': 'Product is in good condition, size 40, colour red.', # duhet mi pas mbi 40 karaktere.
            'general[measurements]': '..',
            'general[yearOfPurchase]': '1900',
            'general[purchasedFrom]': ".",
            'general[images]':'',
            'general[price][currency]': 'GBP',
            'general[price][amount]': '70.00',
            'general[rrp][currency]': 'GBP',
            'general[rrp][amount]': '70',
            'general[supportedCharity]': '',
            'general[donationPercentage]': '0',
            'general[shippingClass]': '24225',
            'general[submit]':'',
            'general[_token]':self.general_token,
        }
        resp_draft = self.s.post(
            url='https://hardlyeverwornit.com/account/sell/product/edit/{0}'.format(self.product_ID),
            data=self.body,
            headers=self.headers,
            )
        with open('aaa.html', 'w', encoding="utf8") as aa:
            aa.write(resp_draft.text)

    def Publish_Product(self,image_ids_):

        img_ids = ', '.join(str(e) for e in image_ids_)
        self.body.update(
            {'general[images]':img_ids,}
        )
        response = self.s.post( 
            url='https://hardlyeverwornit.com/account/sell/product/edit/{0}'.format(self.product_ID),
            data = self.body,
            headers=self.headers)
        if 'Thank you. Your product was submitt' in response.text:
            print('Submited Product with ID:',self.product_ID)
        else:
            print('Not Submited Product')
        # self.html_content('publish',response.text)

    def Delete_Product_ID(self):
        response =self.s.get(url='https://hardlyeverwornit.com/account/sell/product?filter%5Bstate%5D=staff_edit')
        if response.status_code == 200:
            for tr in re.findall(r'<td class="admin-list__actions">(.*?)</form>',response.text,re.I|re.S):
                for id_, crff_ in re.findall(r'sell/product/(\d+)" method="POST">.*?_csrf_token" value="(.*?)"',str(tr),re.I|re.S):
                    payload ={
                        '_method': 'DELETE',
                        '_csrf_token': crff_,
                    }
                    response1 = self.s.post(
                        url='https://hardlyeverwornit.com/account/sell/product/{0}'.format(id_),
                        data = payload,
                        headers=self.headers
                        )
                    if 'Product was deleted' in response1.text:
                        print('Product is deleted with ID:',id_)
                        # self.html_content('deletedID',response1.text)
    # if we have more than >50 products. has to go in each page
    def Delete_Product_All_ID(self):
        # https://hardlyeverwornit.com/account/sell/product?filter%5Bstate%5D=requires_changes&limit=100
        response =self.s.get(url='https://hardlyeverwornit.com/account/sell/product?filter%5Bstate%5D=staff_edit&limit=100')
        if response.status_code == 200:
            check = True
            contentall = response.text
            while check:
                try:
                    for tr in re.findall(r'<td class="admin-list__actions">(.*?)</form>',contentall,re.I|re.S):
                        for id_, crff_ in re.findall(r'sell/product/(\d+)" method="POST">.*?_csrf_token" value="(.*?)"',str(tr),re.I|re.S):
                            print(id_, crff_)
                            payload ={
                                    '_method': 'DELETE',
                                    '_csrf_token': crff_,
                            }
                            response1 = self.s.post(
                                url='https://hardlyeverwornit.com/account/sell/product/{0}'.format(id_),
                                data = payload,
                                headers=self.headers
                                )
                            if 'Product was deleted' in response1.text:
                                print('Product is deleted with ID:',id_)
                    time.sleep(2)
                    go_back=self.s.get(url='https://hardlyeverwornit.com/account/sell/product?filter%5Bstate%5D=staff_edit&limit=100').text
                    contentall =go_back.text
  
                except:
                    check=False
            print('all products are deleted ')

    def html_content(self,page, content):
        with open(str(page) + '.html', 'at') as f: 
            f.write(content)

    def submit_item(self, row):
        row['partner_id'] = ""
        row['error_message'] = ""
        row['partner_url'] = ""
        row['listing_status'] = "FAIL"

        try:
            list_of_image_ids = self.upload_images(row)
        except Exception as e:
            row["error_message"] = "Something went wrong with images"
            self.log_errors(self.listing_id, row['item_id'], row['error_message'])
            return row

        if not list_of_image_ids:
            row['error_message'] = "One or more images have failed!"
            return row

        try:
            partner_id = self.create_draft_listing(row, list_of_image_ids)
        except Exception as e:
            row["error_message"] = "Couldn't create draft listing"
            self.log_errors(self.listing_id, row['item_id'], row['error_message'])
            return row

        if partner_id is None:
            row['error_message'] = "Could not create draft"
            return row

        row['partner_id'] = partner_id
        row['partner_url'] = f''
        row['listing_status'] = "DRAFT"

        try:
            res = self.publish_listing(partner_id)
        except Exception as e:
            row["error_message"] = "Could not publish item"
            self.log_errors(self.listing_id, row['item_id'], row['error_message'])
            return row

        if res.ok:
            row['listing_status'] = "SUCCESS"

        requests.patch(
            url=f"{os.getenv('NESTJS_SERVICE')}/{self.listing_id}/{row['item_id']}",
            data={
                "listingStatus": "SUCCESS",
                "partnerId": row['partner_id'],
                "partnerUrl": row['partner_url']
            }
        )

        return row


if __name__ == '__main__':
    email ='meruerik@saxophonexltd.com'
    password ='grailed@123'
    row ={'images':['https://s3.eu-west-1.amazonaws.com/twig.sales/84fa416c78f24e8caa0724a7890d1dd2', 
    'https://s3.eu-west-1.amazonaws.com/twig.sales/163b77f3a2a04202a05f0509bfb94379',
    'https://s3.eu-west-1.amazonaws.com/twig.sales/84fa416c78f24e8caa0724a7890d1dd2',
    'https://s3.eu-west-1.amazonaws.com/twig.sales/43c82397cea945b6a30c7b0d07191651',
    'https://s3.eu-west-1.amazonaws.com/twig.sales/735f6fccaffa42c3a4b6b1d56e2dd5ec',
    'https://s3.eu-west-1.amazonaws.com/twig.sales/bbc2fdff40a2497c8e17bf755f653c20',
    'https://s3.eu-west-1.amazonaws.com/twig.sales/fa838260b216424395d0c86c020b124b'
        ''
      ]}
    crawl = Hewi()
    crawl.Login(email, password)
    crawl.Product_ID_()
    crawl.create_draft_body()
    image_ids_ = crawl.upload_images(row)
    crawl.Publish_Product(image_ids_)
    # time.sleep(2)
    # crawl.Delete_Product_ID()
    # crawl.Delete_Product_All_ID()

    '''
    Required fields:
      general[mainTaxon]: 5
      general[designer]: 3693
      general[suggestedDesigner]: 
      general[size]: 5
      general[sizeOnLabel]: L
      general[itemCondition]: hardly_ever_worn
      general[fabric]: cotton
      general[colour]: red
      general[nearestColour]: 3
      general[description]: kosova republikkosova republikkosova republikkosova republikkosova republik
      general[measurements]: ..
      general[yearOfPurchase]: 1900
      general[purchasedFrom]: .
      general[images]: 734586,734691,734692,734701,734702
      general[price][currency]: GBP
      general[price][amount]: 45.00
      general[rrp][currency]: GBP
      general[rrp][amount]: 45
      general[supportedCharity]: 
      general[donationPercentage]: 0
      general[shippingClass]: 23915
      general[submit]: 
      general[_token]: 6f97f8d850a465a4.LzKz4VDcpSAGzTJN8Qr4EHq2BQ4TczF1sO8M3dBH9zo.TUbphH217Ghui34qm3mwd0mbY2ZdJlVM1N87vpNzlENOC_iAOOnpUWmlRQ
    '''