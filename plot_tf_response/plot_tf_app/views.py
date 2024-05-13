from django.shortcuts import render
from sympy import plot
from tf_response import plot_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64


@csrf_exempt
def plot_response_api(request):
    if request.method == 'POST':
        try:
            # Get the request data
            data = json.loads(request.body)
            d = data.get('d')
            vin = data.get('vin')
            inductor = data.get('inductor')
            capacitor = data.get('capacitor')
            resistor = data.get('resistor')
            mode = data.get('mode')

            # Validate the input data
            if not all([d, vin, inductor, capacitor, resistor, mode]):
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            if mode not in ['Buck', 'Boost', 'BuckBoost']:
                return JsonResponse({'error': 'Invalid mode'}, status=400)

            # Call the plot_response function
            plot = plot_response(d, vin, inductor, capacitor, resistor, mode)

            plot_base64 = base64.b64encode(plot).decode('utf-8')

            # Return the response as JSON
            response = {
                'img': plot_base64
            }
            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)