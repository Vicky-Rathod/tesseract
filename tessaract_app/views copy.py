from datetime import datetime, date
import json
import os,shutil
import time

import PyPDF2
import boto3
from cffi import FFI
import pikepdf
from pikepdf import Pdf
from django.shortcuts import render
from requests.structures import CaseInsensitiveDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from PyPDF2.generic import RectangleObject
from os import path
from .forms import SingleForm
from . serializers import *
from . models import *
from django.conf import settings
# Create your views here.
##################################
#           Ocr
##################################
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTText, LTLine, LTChar, LTPage
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter
import random
import string
from PIL import Image
import requests
from io import StringIO
def index(request):
    print("request",request)
    return render(request, 'index.html', context={})


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'list': '/list_users/',
        'manual create': '/manual_create/'
    }

    return Response(api_urls)



@api_view(['GET'])
def copyfroms3(request):
    # data = "C:\Users\prana\Downloads"
    # result = json.dumps("data")

    return Response({'data':"arru"})

@api_view(['GET'])
def uploadS3(request):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    password=''
    # Open a PDF document.
    fp = open('C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/toc3.pdf', 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)

    # Get the outlines of the document.
    outlines = document.get_outlines()
    arru =[]
    for (level, title, dest, a, se) in outlines:
        print(level, title,dest,a, se)
        arru.append({
            'level':level,
            'title':title,
            'dest': dest,
            'a':a,
            'se':se
        })
    return Response({'data':arru})

@api_view(['GET'])
def alluser(resuest):
    users = Users.objects.all()
    serializer = userserilizer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def manual_create(resuest):
    # ROOT_PUBLIC()
    # for file in glob(ROOT_PUBLIC('')):
    #     print(file)
    return Response("hello")

@api_view(['GET'])
def merge(resuest):
    img_path = ["C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/300962.jpg",
                "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/convert.pdf"]

    # storing pdf path
    pdf_path = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/convert.pdf"

    array = []
    for path in img_path:
        if(path.lower().endswith(('.png', '.jpg', '.jpeg'))):
            print("true")
            converted = ConvertImgToPDF(path)
            array.append(converted)
            print("true",converted)
        else:
            print("false")
            array.append(path)


    return Response({
            'Success': 200,
            'message': array,
            'link': 'http://127.0.0.1:8000/static/merged1.pdf'
    })


@api_view(['GET'])
def toc(resuest):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open('manual.pdf', 'rb'))

    # get page dimensions
    x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
    print(f'x1, x2: {x1, x2}\ny1, y2: {y1, y2}')

    # add each page in pdf to pdf writer
    num_of_pages = pdf_reader.getNumPages()

    for page in range(num_of_pages):
        current_page = pdf_reader.getPage(page)
        pdf_writer.addPage(current_page)

    # Add Link
    pdf_writer.addLink(
        pagenum=1,  # index of the page on which to place the link
        pagedest=2,  # index of the page to which the link should go
        rect=RectangleObject([ 213 , 595, 280 , 610]),  # clickable area x1, y1, x2, y2 (starts bottom left corner)
        # border
        # fit
    )

    pdf_writer.addLink(
        pagenum=1,  # index of the page on which to place the link
        pagedest=20,  # index of the page to which the link should go
        rect=RectangleObject([ 213 , 575, 280 , 590]),   # clickable area x1, y1, x2, y2 (starts bottom left corner)
        # border
        # fit
    )

    with open(path.abspath('pdf_with_link.pdf'), 'wb') as link_pdf:
        pdf_writer.write(link_pdf)
    return Response({
            'Success': 200,
            'message': 'Manual Create Succesfully',
            'link': 'http://127.0.0.1:8000/static/merged1.pdf'
    })

# @api_view(['GET'])
# def ocr(resuest):
#     fp = open('manual.pdf', 'rb')
#     rsrcmgr = PDFResourceManager()
#     laparams = LAParams()
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     pages = PDFPage.get_pages(fp)
#     array = []
#     pager = []
#     i = 1
#     for page in pages:
#         print('Processing next page...')
#         interpreter.process_page(page)
#         layout = device.get_result()
#         pager = []
#         for lobj in layout:
#             if isinstance(lobj, LTTextBox):
#                 x, y,w, h, text = lobj.bbox[0], lobj.bbox[3],lobj.bbox[1],lobj.bbox[2], lobj.get_text()
#                 # print('At %r is text: %s' % ((x, y,w, h), text))
#                 if(x > 100 and x <= 160):
#                     pager.append({
#                         'x': x,
#                         'y': y,
#                         'width':w,
#                         'height':h,
#                         'text':text.replace("\n","")
#                     })
#         array.append({
#             'page': i,
#             'corrdinates':  pager
#         })
#
#         i += 1
#
#     #     pdf_writer = PdfFileWriter()
#     #     pdf_reader = PdfFileReader(fp)
#     #
#     #     # get page dimensions
#     #     x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
#     #     # print(f'x1, x2: {x1, x2}\ny1, y2: {y1, y2}')
#     #
#     #     # add each page in pdf to pdf writer
#     #     num_of_pages = pdf_reader.getNumPages()
#     #
#     #     for page in range(num_of_pages):
#     #         current_page = pdf_reader.getPage(page)
#     #         pdf_writer.addPage(current_page)
#     #     z = 0
#     #         # Add Link
#     #     for title in array:
#     #         print("pages",z)
#     #         for coor in title['corrdinates']:
#     #             # print("lol", coor['y'])
#     #                 pdf_writer.addLink(
#     #                     pagenum= z,  # index of the page on which to place the link
#     #                     pagedest=1,  # index of the page to which the link should go
#     #                     rect=RectangleObject([coor['x'],coor['y'], coor['height'],coor['width'] ]),  # clickable area x1, y1, x2, y2 (starts bottom left corner)
#     #                     # border
#     #                     # fit
#     #                 )
#     #         z += 1
#     # with open(path.abspath('slipsheetpage1.pdf'), 'wb') as link_pdf:
#     #     pdf_writer.write(link_pdf)
#
#     return Response({
#         'Success': 200,
#         'slipsheet_file': 'http://127.0.0.1:8000/static/slipsheet.pdf',
#         'message': 'OCR Read',
#         'link': array
#     })


@api_view(['POST'])
def get_closeout_manual(request):
    if request.method == 'POST':

        parameter = SingleForm(data=request.data)
        if parameter.is_valid():
            tbl_project = TblProjects.objects.filter(id = request.data['project_id'],isdeleted = 0).first()
            projectData = projectserilizer(tbl_project, many=False)
            if (not projectData):
                 return Response({'success': 0, 'message': 'Project does not exists.'})
            procore_project_id = projectData.data['procore_project_id']
            project_name = projectData.data['project_name']
            company_id = projectData.data['company_id']
            size = 0
            # assign folder path
            Folderpath = os.path.join(
                'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/' + str(
                    company_id) + '/' + str(request.data['project_id']) + '/')

            # get size
            # for path, dirs, files in os.walk(Folderpath):
            #     for f in files:
            #         fp = os.path.join(path, f)
            #         size += os.stat(fp).st_size
            # print(size)
            # print(humanize.naturalsize(size))
            if (size > 1610612736):
                return Response({'success': 0, 'message': 'Project size is above 2GB'})

            # Check Manual Exist()
            checkManual = TblCloseoutManual.objects.filter(project_id=request.data['project_id'],
                                                           closeout_company_id=request.data[
                                                               'closeout_company_id']).order_by('-id').first()
            checkManualExists = TblManualSerilizer(checkManual, many=False)
            print(checkManualExists.data)
            if (checkManualExists.data['version']):
                checkVersion = checkManualExists.data['version']
                versionInc = int(checkVersion) + 1
                historypath = str(company_id) + '/' + str(procore_project_id) + '/closeout_manuals/manual_' + str(
                    procore_project_id) + '_' + str(company_id) + '_V' + str(versionInc) + '.pdf'
                # now = datetime.datetime.utcnow()
                # linkInsert = TblCloseoutManual(manual_link=historypath, version=versionInc,
                #                                date=now.strftime('%Y-%m-%d %H:%M:%S'),
                #                                created_by=request.data['user_id'], status=1,
                #                                project_id=request.data['project_id'], closeout_company_id=company_id,
                #                                created_at=now.strftime('%Y-%m-%d %H:%M:%S'),
                #                                updated_at=now.strftime('%Y-%m-%d %H:%M:%S'))
                # linkInsert.save()
            else:
                versionInc = 0
                historypath = str(company_id) + '/' + str(procore_project_id) + '/closeout_manuals/manual_' + str(
                    procore_project_id) + '_' + str(company_id) + '_V' + str(versionInc) + '.pdf'
                # now = datetime.datetime.utcnow()
                # linkInsert = TblCloseoutManual(manual_link=historypath, version=versionInc,
                #                                date=now.strftime('%Y-%m-%d %H:%M:%S'),
                #                                created_by=request.data['user_id'], status=1,
                #                                project_id=request.data['project_id'], closeout_company_id=company_id,
                #                                created_at=now.strftime('%Y-%m-%d %H:%M:%S'),
                #                                updated_at=now.strftime('%Y-%m-%d %H:%M:%S'))
                # linkInsert.save()

            # API_ENDPOINT = "https://web.closeoutdaddy.com/webapi/public/api/closeout_manual_email"
            # data = {'project_id': request.data['project_id'],
            #         'type': 'start',
            #         'closeout_company_id': request.data['closeout_company_id']}
            # r = requests.post(url=API_ENDPOINT, data=data)
            # extracting response text
            # pastebin_url = r.text
            # print("The pastebin URL is:%s" % pastebin_url)
            #project Index


            project_index = TblProjectIndex.objects.filter(project_id=request.data['project_id'])
            index_project = Indexerilizer(project_index, many=True)

            for index in index_project.data:
                # Drawings pdf Merge
                if (index['title'] == "Drawings"):
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Section_1_Drawing.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/slipsheet_drawing_' + str(procore_project_id)+ '_' + str(company_id) + '.pdf'
                        ]
                    drawingTrades = TblTrades.objects.filter(project_id=procore_project_id).order_by('name')
                    tradedata = tradeserilizer(drawingTrades, many=True)

                    for trade in tradedata.data:
                        print("tradedataa ------ ", trade['name'])
                        drawings_pdfs = TblDrawings.objects.filter(project_id=projectData.data['procore_project_id'],
                                                                   trade_id= trade['procore_drawing_discipline_id'],
                                                                   closeout_company_id=request.data['closeout_company_id'])
                        WithSerilizer = Drawingserilizer(drawings_pdfs, many=True)
                        for path in WithSerilizer.data:
                                base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                file_path =  base_url + str(path['closeout_attachment'])
                                if os.path.isfile(file_path):
                                    # print("filebase",str(file_path) )
                                    drawing_indexes.append(file_path)
                                else:
                                    pass
                    # drawing_indexes.extend(drawings_pdfs.data[''])

                if (index['title'] == 'Specifications'):
                     drawing_indexes = [
                            'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Section_5_Specification.pdf',
                            'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/slipSheet_specification_' + str(
                                procore_project_id) + '_' + str(company_id) + '.pdf'
                        ]
                     # Check PROCORE SPEC SEC ID
                     Specifications_pdf = TblSpecifications.objects.filter(project_id=projectData.data['procore_project_id'],
                                                               closeout_company_id=request.data['closeout_company_id'])
                     specificationData = Specificationserilizer(Specifications_pdf, many=True)
                     for specPath in specificationData.data:
                         # Get PDF URL In TBL_Spec_section
                         Spec_pdf_url = TblSpecSections.objects.filter(project_id=projectData.data['procore_project_id'],closeout_company_id=request.data['closeout_company_id'],procore_spec_sec_id = specPath['current_revision_id'])
                         speciPDFData = Spec_urlserilizer(Spec_pdf_url, many=True)
                         # break
                         if(speciPDFData.data):
                             base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                             file_path = base_url + str(speciPDFData.data[0]['attachment'])
                             # print(specPath['id'],speciPDFData.data[0]['attachment'])
                             if os.path.isfile(file_path):
                                 # print("filebase", str(file_path))
                                 if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                     converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                     drawing_indexes.append(converted)
                                 else:
                                     drawing_indexes.append(file_path)
                             else:
                                 pass
                         else:
                            pass

                if (index['title'] == 'RFI'):
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Section_3_Rfis.pdf' ,
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/slipsheet_Index_Rfi_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    # Check PROCORE SPEC RFI
                    attArr = []
                    RFI_pdf = TblRfis.objects.filter(
                        project_id=projectData.data['procore_project_id'],
                        closeout_company_id=request.data['closeout_company_id']).order_by('date_initiated')
                    RFIData = RFIserilizer(RFI_pdf, many=True)
                    indx = 1
                    for RfiPath in RFIData.data:
                            # Check Rfi Question
                            Question_Attachment_url = TblRfiQuestions.objects.filter(rfi_id=RfiPath['procore_rfi_id'],closeout_company_id=request.data['closeout_company_id']).order_by('-question_date')
                            RFIQuesATTAData = RFIQuesAttachserilizer(Question_Attachment_url, many=True)
                            # print("datata",RFIQuesATTAData.data)
                            for finalData in RFIQuesATTAData.data:
                                # Check Rfi Question Attachment
                                # print("closeout_company_id=",request.data['closeout_company_id'])
                                Question_Attachment_paths = TblRfiQuestionsAttachments.objects.filter(question_id=finalData['procore_question_id'],closeout_company_id=request.data['closeout_company_id'])
                                RFIQuesATTAPath = RFIQuesPathserilizer(Question_Attachment_paths, many=True)
                                #  print("QuestionData", RFIQuesATTAPath.data)
                                base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/tempPDF/"
                                file_path = base_url + str(request.data['closeout_company_id']) + '/' + str(
                                    projectData.data['procore_project_id']) + '/tmp_' + RfiPath['number'] + '.pdf'
                                # print("base url rfi",file_path);
                                # print("datas",RfiPath['number'])
                                if os.path.isfile(file_path):
                                    attArr.append(file_path)
                                    indx += 1
                                else:
                                    pass
                                if (RFIQuesATTAPath.data):
                                    for quesPath in RFIQuesATTAPath.data:
                                        base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                        file_path = base_url + str(quesPath['closeout_attachment_url'])

                                        if os.path.isfile(file_path):
                                            #  print("filebase", str(file_path))
                                            if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                                converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                                attArr.append(converted)
                                            else:
                                                attArr.append(file_path)
                                        else:
                                            pass
                                else:
                                    pass
                        # Get PDF URL In TBL_Spec_section
                            Rfi_pdf_url = TblRfiAnswers.objects.filter(rfi_id=RfiPath['procore_rfi_id'],closeout_company_id=request.data['closeout_company_id']).order_by('-answer_date')
                            RFIPDFData = RFIAnsserilizer(Rfi_pdf_url, many=True)
                            for RFIAttachment in RFIPDFData.data :
                                Rfi_Attachment_url = TblRfiAttachments.objects.filter(answer_id=RFIAttachment['procore_answer_id'],closeout_company_id=request.data['closeout_company_id'])
                                RFIATTAData = RFIAttachserilizer(Rfi_Attachment_url, many=True)

                                for finalData in RFIATTAData.data:
                                    if (finalData):
                                        base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                        file_path = base_url + str(finalData['closeout_attachment_url'])

                                        if os.path.isfile(file_path):
                                            #  print("filebase", str(file_path))
                                            if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                                converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                                attArr.append(converted)
                                            else:
                                                attArr.append(file_path)
                                        else:
                                            pass
                                    else:
                                        pass
                    drawing_indexes.extend(attArr)
                    print("Rfo",attArr)

                if (index['title'] == "Submittals"):
                    attArr = []

                    drawing_indexes = [
                            'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Section_2_Submittals.pdf',
                            'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/slipSheet_submittals_' + str(procore_project_id)+ '_' + str(company_id) + '.pdf'
                            ]
                    pecDivision = TblSpecSectionDivisions.objects.filter(
                        project_id=projectData.data['procore_project_id']).filter(
                        closeout_company_id=request.data['closeout_company_id'])
                    for i in pecDivision:
                        approveAubmmitals = TblApproveSubmittals.objects.filter(project_id=projectData.data['procore_project_id'],
                                                                   closeout_company_id=request.data['closeout_company_id']).filter(sort_number = i.number)
                        WithSerilizer = ApprovedSubmittalserilizer(approveAubmmitals, many=True)
                        for path in WithSerilizer.data:
                            maxdate = TblSubmittalWorkflow.objects.filter(submittal_id=path['procore_submittal_id']).order_by('-returned_date').first()

                            maxdateseilizer = workflowSubmittalserilizer(maxdate, many=False)
                            if(maxdateseilizer.data['returned_date']):
                                latestWorkflow = TblSubmittalWorkflow.objects.filter(submittal_id=path['procore_submittal_id'],returned_date = maxdateseilizer.data['returned_date']).order_by('-id').first()
                                latestWorkflowDatas = workflowSubmittalserilizers(latestWorkflow, many=False)
                            else:
                                latestWorkflow = TblSubmittalWorkflow.objects.filter(
                                    submittal_id=path['procore_submittal_id']).order_by('-id').first()
                                latestWorkflowDatas = workflowSubmittalserilizers(latestWorkflow, many=False)

                            sumittalsattachmentData = TblSubmittalAttachments.objects.filter(submittal_id=latestWorkflowDatas.data['procore_submittal_id'],procore_workflow_id=latestWorkflowDatas.data['procore_workflow_id'],project_id=projectData.data['procore_project_id'],
                                                                   closeout_company_id=request.data['closeout_company_id'] ).order_by('-id')
                            submittalsAtSerilizers = submittalsAttachmentSerilizer(sumittalsattachmentData, many=True)
                            for finalData in submittalsAtSerilizers.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['closeout_attachment_url'])

                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                    drawing_indexes.extend(attArr)
                    print("submittals logs",drawing_indexes)
                    print("submitals end")
                if (index['title'] == "Warranties"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/' + str(index['title']) + '.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Warranties_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id= request.data['project_id'],type = index['title'],isdeleted = 0)
                    closoeutItems=CloseoutItemsSerilizer(chkCloseoutFiles_w,many = True)
                    # print(closoeutItems.data)
                    if(closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(closeout_item_id = AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "O & M Manuals"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/' + str(
                            index['title']) + '.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/O & M Manuals_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='O & M Manuals', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Training / Demonstration videos"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Training&Demonstration_Videos' + '.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Training - Demonstration videos_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Training/Demonstration videos', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "As-builts"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/As-builts.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/As-builts_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='As-Builts', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Commissioning"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Commissioning.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Commissioning_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Commissioning', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Liens"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Liens.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Liens_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Liens', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Miscellaneous documents"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/documents.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Miscellaneous documents_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Miscellaneous documents', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Reports"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Reports.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Reports_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Reports', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Certificates"):
                    attArr = []
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Certificates.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/closeoutItems/Certificates_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]
                    chkCloseoutFiles_w = TblCloseoutItems.objects.filter(project_id=request.data['project_id'],
                                                                         type='Certificates', isdeleted=0)
                    closoeutItems = CloseoutItemsSerilizer(chkCloseoutFiles_w, many=True)
                    # print(closoeutItems.data)
                    if (closoeutItems.data):
                        for AttCloseout in closoeutItems.data:
                            CloseoutAttachement = TblCloseoutItemUploads.objects.filter(
                                closeout_item_id=AttCloseout['id'])
                            closoeutAttpath = CloseoutAttachmentSerilizer(CloseoutAttachement, many=True)
                            for finalData in closoeutAttpath.data:
                                if (finalData):
                                    base_url = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/"
                                    file_path = base_url + str(finalData['file'])
                                    if os.path.isfile(file_path):
                                        if (file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                            converted = ConvertImgToPDF(file_path,str(procore_project_id),str(company_id),index['title'])
                                            attArr.append(converted)
                                        else:
                                            attArr.append(file_path)
                                    else:
                                        pass
                                else:
                                    pass
                        drawing_indexes.extend(attArr)
                if (index['title'] == "Team"):
                    drawing_indexes = [
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/section pages/Section_6_Contacts.pdf',
                        'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/slip sheets/slipSheet_Project_Contacts_' + str(
                            procore_project_id) + '_' + str(company_id) + '.pdf'
                    ]

                merg_pdf(drawing_indexes,str(procore_project_id),str(company_id),index['title'])
            indexSetting = TblProjectIndex.objects.filter(project_id=request.data['project_id'])
            IndexArray = TblindexSerilizer(indexSetting, many=True)
            CoverPage = TblCoverPages.objects.filter(project_id=request.data['project_id'],closeout_company_id=request.data['closeout_company_id']).first()
            CoverpageData = CoverPageSerilizer(CoverPage, many=False)

            tableofcontent = TblIndexPages.objects.filter(project_id=request.data['project_id']).first()
            tablecontentData = TableContetserilizer(tableofcontent, many=False)
            public_path = 'C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/public/'
            parent_dir = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/"

            path = os.path.join(parent_dir, str(company_id) + '/' + str(procore_project_id) + '/' + 'tempManual/temp')
            fileToMerge = [
                os.path.join(public_path + CoverpageData.data['pdf_path'].replace("*", "_")),
                os.path.join(public_path + tablecontentData.data['pdf_path'].replace("*", "_"))
            ]
            for section in IndexArray.data:
                print(section['section_id'])
                if(section['section_id']== 1):
                    # print("drawings")
                    fileToMerge.append(os.path.join(path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 2):
                    # print("Specifications")
                    fileToMerge.append(os.path.join(
                        path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 3):
                    # print("Rfi")
                    fileToMerge.append(os.path.join(
                        path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 4):
                    # print("Submittals")
                    fileToMerge.append(os.path.join(
                        path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 5):
                    # print("Warranties")
                    fileToMerge.append(os.path.join(
                        path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 6):
                    # print("O & M Manuals")
                    fileToMerge.append(os.path.join(
                        path + section['title'] + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 7):
                    # print("As-builts")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 8):
                    # print("Training / Demonstration videos")
                    fileToMerge.append(os.path.join(
                        path + 'Training  Demonstration videos'+ '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 9):
                    # print("Affidavits & Bonds")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 10):
                    # print("Liens")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 11):
                    # print("Miscellaneous documents")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 12):
                    # print("Reports")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 13):
                    # print("Certificates")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))
                elif (section['section_id'] == 14):
                    # print("Team")
                    fileToMerge.append(os.path.join(
                        path + section['title'].replace("/", "") + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'))

            savepath =  Finalmerge_pdf(fileToMerge,str(procore_project_id),str(company_id),versionInc)
            # historypath = 'manual/'+ str(company_id) + '/' + str(procore_project_id)+'/manual_' + str(procore_project_id) + '_' + str(company_id) + '.pdf'
            # now = datetime.datetime.utcnow()
            # TblManualHistory = TblCloseoutManual(manual_link=historypath, version=0, date=now.strftime('%Y-%m-%d %H:%M:%S'),created_by= request.data['user_id'],status=2,project_id= request.data['project_id'],closeout_company_id=company_id,created_at=now.strftime('%Y-%m-%d %H:%M:%S'),updated_at=now.strftime('%Y-%m-%d %H:%M:%S'))
            # TblManualHistory.save()
            checkManual = TblCloseoutManual.objects.filter(project_id=request.data['project_id'],
                                                           closeout_company_id=request.data[
                                                               'closeout_company_id']).order_by('-id').first()
            checkManualExists = TblManualSerilizer(checkManual, many=False)
            updateManual = TblCloseoutManual.objects.filter(id=checkManualExists.data['id']).update(status=2)
            API_ENDPOINT = "https://web.closeoutdaddy.com/webapi/public/api/closeout_manual_email"
            data = {'project_id': request.data['project_id'],
                    'type': 'end',
                    'closeout_company_id': request.data['closeout_company_id']}
            r = requests.post(url=API_ENDPOINT, data=data)

            pastebin_url = r.text
            # print("The pastebin URL is:%s" % pastebin_url)
            return Response({'success': 0,'path': savepath ,'message': "Manual Create Successfully"})
        else:
            # print(parameter.errors)
            return Response({'success': 0, 'message': parameter.errors})

def merg_pdf(drawing_indexes,procore_project_id,company_id,title):
    parent_dir= "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/"

    path = os.path.join(parent_dir, str(company_id) +'/'+ str(procore_project_id) +'/'+'tempManual')

    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully")
    except OSError as error:
        print("Directory '%s' can not be created")
    pdf = Pdf.new()
    sectionocr = []
    for file in drawing_indexes:
         # print("userfile",file)
         try:
             src = Pdf.open(file)
             # pdf.pages.extend(src.pages)
             if(title == 'Drawings'):
                 read_pdf = PyPDF2.PdfFileReader(file)
                 num_pages = read_pdf.getNumPages()

                 sectionocr.append({'pages': num_pages})
             pdf.pages.extend(src.pages)
         except pikepdf.PasswordError as error:
             print('password required')
             pass
         except pikepdf.PdfError as results:
              print('cannot open file')
              pass



    # pdf.save('C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/merged1.pdf')
    savePath = os.path.join(path +'/temp'+ str(title.replace("/", "")) + '_' + str(procore_project_id) + '_' + str(company_id) + '.pdf')
    pdf.save(savePath)
    src.close()
    pdf.close()


    # print("start")
    # time.sleep(20)
    ocrs = ocr(drawing_indexes, sectionocr, savePath,title,path)
    # time.sleep(10)
    # print("end")
    # os._exit("n")
    return "ocrs"



def ConvertImgToPDF(img_path,procore_project_id,company_id,title):
    # storing pdf path
    parent_dir = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/"

    path = os.path.join(parent_dir, str(company_id) + '/' + str(procore_project_id) + '/' + 'convertPdf/')

    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully")
    except OSError as error:
        print("Directory '%s' can not be created")

    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    pdf_path = path + str(file_name) + '.pdf'
    image1 = Image.open(img_path)
    im1 = image1.convert('RGB')
    im1.save(pdf_path)
    return pdf_path

def Finalmerge_pdf(fileToMerge,procore_project_id,company_id,versionInc):
    parent_dir = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/"
    FinalManualPaths = os.path.join(parent_dir, str(company_id) + '/' + str(procore_project_id) + '/' + 'manuals')
    try:
        os.makedirs(FinalManualPaths, exist_ok=True)
        print("Directory '%s' created successfully")
    except OSError as error:
        print("Directory '%s' can not be created")
    pdf = Pdf.new()
    sectionocr =[]
    for file in fileToMerge:
        # print("userfile", file)
        try:
            src = Pdf.open(file)
            read_pdf = PyPDF2.PdfFileReader(file)
            num_pages = read_pdf.getNumPages()
            sectionocr.append({'pages': num_pages})
            pdf.pages.extend(src.pages)

        except pikepdf.PasswordError as error:
            print('password required')
            pass
        except pikepdf.PdfError as results:
            print('cannot open file')
            pass

    # pdf.save('C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/merged1.pdf')
    savePath = os.path.join(
        FinalManualPaths + '/manual_' + str(procore_project_id) + '_' + str(
            company_id) + '.pdf')

    pdf.save(savePath)
    src.close()
    pdf.close()

    ocrTask = ocrlinking(fileToMerge,sectionocr,savePath)

    # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    # bucket = s3.Bucket('hsm-bucket2')
    # with open(savePath, 'rb') as file:
    #     bucket.put_object(Key=str(company_id) + '/' + str(procore_project_id) + '/closeout_manuals/manual_' + str(
    #                 procore_project_id) + '_' + str(company_id) + '_V' + str(versionInc) + '.pdf', Body=file,ACL ='public-read',ContentType="application/pdf")
    return ocrTask

def ocrlinking(fileToMerge,sectionocr,savepath):

    fp = open(fileToMerge[1], 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    pager = []
    i = 1
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for pagenumber, page in enumerate(
            PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                              check_extractable=True)):
        # print(pagenumber)
        if pagenumber % 2 == 0:
            # print("even page number")
            interpreter.process_page(page)
            layout = device.get_result()
            pager = []
            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    x, y, w, h, text = lobj.bbox[0], lobj.bbox[3], lobj.bbox[1], lobj.bbox[2], lobj.get_text()
                    # print('At %r is text: %s' % ((x, y,w, h), text))
                    if (x > 100 and x <= 160):
                        pager.append({
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'text': text.replace("\n", "")
                        })

    # print('Processing s...', pager)
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(savepath)

    # get page dimensions
    x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
    # print(f'x1, x2: {x1, x2}\ny1, y2: {y1, y2}')

    # add each page in pdf to pdf writer
    num_of_pages = pdf_reader.getNumPages()

    for para in range(num_of_pages):
        current_page = pdf_reader.getPage(para)
        pdf_writer.addPage(current_page)
        #slice array of 1st two pages
        arr = slice(2, None, 1)
        pagesflinking = sectionocr[arr]
        # print("Linkingarray",pagesflinking)
        # Add Link
    print("Linkingarray",pagesflinking)
    zarray = 2
    # arrpages = slice(None, None, 1)
    # pagerar = pager[arrpages]
    print("pager",pager)
    for idx,coor in enumerate(pager):
        # print("pages",idx)
        print("pages", zarray)
        # print("lol", coor['y'])
        pdf_writer.addLink(
            pagenum= 1,  # index of the page on which to place the link
            pagedest= zarray,  # index of the page to which the link should go
            rect=RectangleObject([coor['x'],coor['y'], coor['height'],coor['width']]),  # clickable area x1, y1, x2, y2 (starts bottom left corner)
            # border
            # fit
        )
        print("data",pagesflinking[idx]['pages'])
        zarray += pagesflinking[idx]['pages'] | 0

    with open(savepath, 'wb') as link_pdf:
        pdf_writer.write(link_pdf)
    fp.close()
    device.close()
    return pager

@api_view(['GET'])
def convert_pdf_to_txt(request):
    data = TblProjects.objects.filter(company_id = 1,id=19).select_related("company").first()
    print(data)
    return "dac"


# @api_view(['GET'])
def ocr(fileToMerge,sectionocr,savepath,title,path):
    if (title == 'Drawings'):
        fp = open(fileToMerge[1], 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.all_texts = True
        laparams.detect_vertical = False
        laparams.line_margin = 0.1
        laparams.char_margin = 0.1
        laparams.word_margin = 0.1
        laparams.boxes_flow = 0.1

        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)
        array = []
        i=0
        for page in pages:
            interpreter.process_page(page)
            layout = device.get_result()
            pager = []
            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    x, y,w, h, text = lobj.bbox[0], lobj.bbox[3],lobj.bbox[1],lobj.bbox[2], lobj.get_text()
                    # print('At %r is text: %s' % ((x, y,w, h), text))
                    if(x > 69 and x <= 160):
                        pager.append({
                            'x': x,
                            'y': y,
                            'width':w,
                            'height':h,
                            'text':text.replace("\n"," ")
                        })
            array.append({
                'page': i,
                'corrdinates':  pager
            })

            i += 1
        print('Processing next page...', array)
        fp.close()
        device.close()
        sc = open(savepath, 'rb')
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(sc)

        # get page dimensions
        x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
        # print(f'x1, x2: {x1, x2}\ny1, y2: {y1, y2}')

        # add each page in pdf to pdf writer
        num_of_pagess = pdf_reader.getNumPages()

        for page in range(num_of_pagess):
            current_page = pdf_reader.getPage(page)
            pdf_writer.addPage(current_page)
        print("Linkingarrayunder", num_of_pagess)
        z = 1
        pagen = 2
        print("lol", array)
        # Add Link
        for title in array:
            for coor in title['corrdinates']:

                print("pages", pagen)
                pdf_writer.addLink(
                    pagenum= 1,  # index of the page on which to place the link
                    pagedest=pagen,  # index of the page to which the link should go
                    rect=RectangleObject([coor['x'],coor['y'], coor['height'],coor['width'] ]),  # clickable area x1, y1, x2, y2 (starts bottom left corner)
                    # border
                    # fit
                )
                z += 1
                pagen +=1
        savePaths = os.path.join(path +'/temp_drawings.pdf')

        with open(savePaths, 'wb') as link_pdf:
            pdf_writer.write(link_pdf)

        sc.close()
        device.close()
        os.remove(savepath)
        os.rename(savePaths, savepath)
    return "True"




@api_view(['GET'])
def training_data_company(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']
        access_token = request.GET['access_token']
        #############################[Emp Dire]#############################################
        response = requests.get(
            f'https://e5de83ed382e15279d3c8f9ee648df5ae1a848bf:x@api.bamboohr.com/api/gateway.php/skilesgroup/v1/employees/directory',
            headers={"Accept": "application/json"}
        )
        empData = response.json()

        if "errors" in empData:
            return Response({"Key Error": "Invalid Emp Data"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            emp_list = empData['employees']
        #############################[procore emp Dire]#############################################
        response = requests.get(
            f'https://api.procore.com/rest/v1.0/projects/{project_id}/users',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = response.json()
        if "errors" in data:
            return Response({"Key Error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)

        finalempdata = []
        for bamemp in emp_list:
            for proemp in data:
                if(bamemp['workEmail'] == proemp['email_address']):
                    finalempdata.append(bamemp)
        #############################[Master Traing Type]#############################################
        Master_train = requests.get(
            f'https://e5de83ed382e15279d3c8f9ee648df5ae1a848bf:x@api.bamboohr.com/api/gateway.php/skilesgroup/v1/training/type',
            headers={"Accept": "application/json"}
        )
        Master_train_type = Master_train.json()

        if "errors" in empData:
            return Response({"Key Error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Traning_type_data = Master_train_type

        #############################[Traing Data Emp Wise]#############################################
        final_training_data = []
        for i in finalempdata:
            Employee_type_data_train = requests.get(
                f"https://e5de83ed382e15279d3c8f9ee648df5ae1a848bf:x@api.bamboohr.com/api/gateway.php/skilesgroup/v1/training/record/employee/{i['id']}",
                headers={"Accept": "application/json"}
            )
            Master_employee_type = Employee_type_data_train.json()
            if Master_employee_type!= []:
                for j in  Master_employee_type.values():
                    for k in Traning_type_data.values():
                        if j['type'] == k['id']:
                            j['traning_data'] = k
                            j['employee_name']= i['displayName']
                            j['employee_designation']= i['jobTitle']
                            final_training_data.append(j)

            if "errors" in empData:
                return Response({"Key Error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Employee_type_data = Master_employee_type
        return Response(final_training_data,
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def RFIMerge(request):
    if request.method == 'POST':
        # data = request.POST['data']
        # project_id = request.POST['project_id']
        # company_id = request.POST['company_id']
        data = {
            "project_id": 11,
            "company_id":25,
             "data" :[
                 {
                     "filename": "RFI-20-Confirmation_of_the_weather_tomorrow.pdf",
                     "url": ["C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/25/11/3. Rfis/image544004.png",
                             "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/25/11/3. Rfis/image633007.png",
                             "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/25/11/3. Rfis/image679006.png",
                             ]
                 }
             ]
            }

        print("datas", request.POST['data'])
        data = request.POST['data']
        return Response(json.loads(data))
        company_id = data['company_id']
        project_id = data['project_id']

        parent_dir = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/"
        FinalManualPaths = os.path.join(parent_dir, str(company_id) + '/' + str(project_id) + '/' + 'mergerfis')
        try:
            os.makedirs(FinalManualPaths, exist_ok=True)
            print("Directory '%s' created successfully")
        except OSError as error:
            print("Directory '%s' can not be created")
        pdf = Pdf.new()
        src = pdf
        sectionocr = []
        for rfi in data['data']:
            for file in rfi['url']:
                print("userfile", file)
                if os.path.isfile(file):
                    if (file.lower().endswith(('.png', '.jpg', '.jpeg'))):
                        converted = ConvertImgToPDFforrfi(file, str(project_id), str(company_id))
                        file = converted
                        # attArr.append(converted)
                    else:
                        # attArr.append(file_path)
                        file = file

                try:
                    src = Pdf.open(file)
                    read_pdf = PyPDF2.PdfFileReader(file)
                    num_pages = read_pdf.getNumPages()

                    sectionocr.append({'pages': num_pages})
                    pdf.pages.extend(src.pages)

                except pikepdf.PasswordError as error:
                    print('password required')
                    pass
                except pikepdf.PdfError as results:
                    print('cannot open file')
                    pass

            # pdf.save('C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/static/merged1.pdf')
            savePath = os.path.join(FinalManualPaths  + '/' +  rfi['filename'])

            pdf.save(savePath)
            src.close()
            pdf.close()

    return Response("pdf created successfully",
                    status=status.HTTP_200_OK)




def ConvertImgToPDFforrfi(img_path,procore_project_id,company_id):
    # storing pdf path
    parent_dir = "C:/Users/prana/Desktop/Bitbucket repo/closeout-django/webapi/storage/app/public/"

    path = os.path.join(parent_dir, str(company_id) + '/' + str(procore_project_id) + '/mergerfis/' + 'convertPdf/')

    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '%s' created successfully")
    except OSError as error:
        print("Directory '%s' can not be created")

    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    pdf_path = path + str(file_name) + '.pdf'
    image1 = Image.open(img_path)
    im1 = image1.convert('RGB')
    im1.save(pdf_path)
    return pdf_path


# =======================QR CODE=================================#

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
import time
import os


SELECTORS = {
    'LOADING': "progress",
    'INSIDE_CHAT': "document.getElementsByClassName('two')[0]",
    'QRCODE_PAGE': "body > div > div > .landing-wrapper",
    'QRCODE_DATA': "div[data-ref]",
    'QRCODE_DATA_ATTR': "data-ref",
    'SEND_BUTTON': 'div:nth-child(2) > button > span[data-icon="send"]'
}
from django.http import FileResponse
from PIL import Image
from io import BytesIO
import base64

@api_view(['GET'])
def qrcode(request):
    page = webdriver.Chrome('C:/Users/prana/Desktop/Bitbucket repo/closeout-django/closeout/chromedriver.exe')
    page.get("https://web.whatsapp.com")

    wait = WebDriverWait(page, 60000)
    time.sleep(2)
    print(SELECTORS['QRCODE_DATA'])
    img = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS['QRCODE_DATA'])))
    data = Image.open(BytesIO(base64.b64decode(img)))
    return FileResponse(data)


@api_view(['GET'])
def busybusy(request):
    if request.method == 'GET':
        start_date = '2021-11-27'
        end_date = '2021-12-27'
        one = datetime.fromisoformat(start_date)
        two = datetime.fromisoformat(end_date)
        url = f"https://export.busybusy.io/?start=2021-11-27 00:00:00&end=2021-12-27 23:59:59"

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["muteHttpExceptions"] = "true"
        headers["Key-Authorization"] = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJidXN5YnVzeS12My1tZW1iZXItc2Vzc2lvbiIsImlhdCI6MTY1MTU4MDE3MSwic3ViIjoiNjkyOTQ5OCJ9.P13Th6aH5yKwOSUofUO9574wHFqIAdPnzgb2A1xQuxg"
        print()
        resp = requests.get(url, headers=headers, )
        from io import StringIO
        io = StringIO()
        data=json.decoder(resp)
        # data=io.getvalue()
        # data = json.dumps(resp.text)
        return Response( data,
                        status=status.HTTP_200_OK)
    return Response("error",
                    status=status.HTTP_200_OK)