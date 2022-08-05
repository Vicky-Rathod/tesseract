from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import *
from rest_framework.decorators import api_view
import requests
import json


@api_view(['GET'])
def procoreCommitments(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']
        access_token = request.GET['access_token']
        response = requests.get(
            f'https://api.procore.com/rest/v1.0/commitments?project_id={project_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = response.json()

        if "errors" in data:
            return Response({"Key Error":"Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
        budget = []
        final_dict = {}
        for commitment in data:
            budget.append({
                'title':commitment['title'],
                'status':commitment['status'],
                'description':commitment['description'],
                'executed':commitment['executed'],
                'vendor':commitment['vendor'].get('name') or None
            })
        contract_payment_response = requests.get(
            f'https://api.procore.com/rest/v1.0/purchase_order_contracts?project_id={project_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        contract_data = response.json()

        return Response(contract_data,
                        status=status.HTTP_200_OK)


@api_view(['GET'])
def ProjectDates(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']
        company_id = request.GET['company_id']
        access_token = request.GET['access_token']
        response = requests.get(
            f'https://api.procore.com/rest/v1.0/projects/{project_id}?company_id={company_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = response.json()

        if "errors" in data:
            return Response({"Key Error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
        dates = {}
        dates['start_date']=data['start_date']
        dates['completion_date'] = data['completion_date']
        dates['actual_start_date'] = data['actual_start_date']
        dates['projected_finish_date'] = data['projected_finish_date']

    return Response(dates,
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def inspections(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']
        access_token = request.GET['access_token']
        response = requests.get(
            f'http://api.procore.com/rest/v1.0/projects/{project_id}/checklist/lists',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = response.text
        print(data);
        if "errors" in data:
            return Response({"Key Error":"Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)

        budget = []
        final_dict = {}
        tojson = json.loads(data)
        for i,j in enumerate(tojson):
            print(j)
            final_dict.clear()
            final_dict['list_template_name'] = j.get("list_template_name") or None
            final_dict['description'] = j.get("description") or None
            final_dict['status'] = j.get("status") or None
            final_dict['inspection_date'] = j.get("inspection_date") or None
            final_dict['closed_at'] = j.get("closed_at") or None
            final_dict['location'] = j.get("location") or None
            if(j['responsible_contractor'] != None ):
                final_dict['responsible_contractor'] = j['responsible_contractor'].get("name") or None
            elif(j['closed_by'] != None):
                final_dict['closed_by'] = j['closed_by'].get("name") or None
            elif (j['date_closed'] != None):
                final_dict['date_closed'] = j.get("closed_at") or None
                final_dict['assignee'] = j['closed_by'].get("name") or None
            final_dict['signer'] = j.get("signature_requests") or None
            final_dict['closed_by'] = j.get("due_date") or None
            final_dict['item_count'] = j.get("item_count") or None
            final_dict['deficient_item_count'] = j.get("deficient_item_count") or None
            final_dict['conforming_item_count'] = j.get("conforming_item_count") or None
            final_dict['neutral_item_count'] = j.get("neutral_item_count") or None
            final_dict['not_applicable_item_count'] = j.get("not_applicable_item_count") or None
            final_dict['trade'] = j.get("trade") or None
            final_dict['specification_section'] = j.get("specification_section") or None


        return Response( budget ,
                        status=status.HTTP_200_OK)




@api_view(['GET'])
def all_project(request):
    if request.method == 'GET':
        company_id = request.GET['company_id']
        access_token = request.GET['access_token']
        response = requests.get(
            f'http://api.procore.com/rest/v1.0/companies/{company_id}/projects',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = response.json()
        # print(data);
        if "errors" in data:
            return Response({"Key Error":"Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)


        return Response( data ,
                        status=status.HTTP_200_OK)
