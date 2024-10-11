#Simón Diego Canales Carvajal, simon.canales@alumnos.uv.cl
import sys
import getopt
import requests

def consultar_mac(mac_address):
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Obtener el valor del fabricante o mostrar "Not found" si es None o está vacío
            fabricante = data.get('company')
            if not fabricante:
                fabricante = "Not found"
            
            # Formato de salida con alineación
            resultado = (
                f"MAC address    : {mac_address}\n"
                f"Fabricante     : {fabricante}\n"
                f"Tiempo de respuesta {int(response.elapsed.total_seconds() * 1000)}ms"
            )
            return resultado
        else:
            return f"Error: No se pudo consultar la MAC {mac_address}"
    except requests.RequestException as e:
        return f"Error: {e}"

def consultar_arp():
    # Simulación de la tabla ARP
    arp_data = {
        "00:01:97:bb:bb:bb": "Cisco",
        "b4:b5:fe:92:ff:c5": "Hewlett Packard",
        "00:E0:64:aa:aa:aa": "Samsung",
        "AC:F7:F3:aa:aa:aa": "Xiaomi"
    }
    result = "MAC/Vendor:\n"
    for mac, vendor in arp_data.items():
        result += f"{mac} / {vendor}\n"
    return result

def main(argv):
    mac_address = None
    show_arp = False

    try:
        opts, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
        print(f"Argumentos recibidos: {opts}")  # Depuración: para verificar los argumentos recibidos
    except getopt.GetoptError:
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
            sys.exit()
        elif opt in ("--mac"):
            mac_address = arg
        elif opt in ("--arp"):
            show_arp = True

    # Verificamos que el usuario haya ingresado o bien una MAC o la opción de ver la tabla ARP
    if mac_address:
        print(consultar_mac(mac_address))  # Se imprime el resultado de la consulta a la API
    elif show_arp:
        print(consultar_arp())  # Se imprime la tabla ARP simulada
    else:
        # Mensaje de uso correcto si no se proporcionan argumentos válidos
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')

# Asegurarse de que el script se ejecute solo si es llamado directamente
if __name__ == "__main__":
    main(sys.argv[1:])
