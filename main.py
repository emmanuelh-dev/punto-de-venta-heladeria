import json
class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f'{self.nombre} - ${self.precio:.2f} - Stock: {self.stock}'

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pedidos = []

    def agregar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def total_gastado(self):
        return sum(p.total for p in self.pedidos)

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []
        self.total = 0.0

    def agregar_item(self, producto, cantidad):
        if producto.stock >= cantidad:
            producto.stock -= cantidad
            self.items.append((producto, cantidad))
            self.total += producto.precio * cantidad
        else:
            print(f"No hay suficiente stock de {producto.nombre}")

    def aplicar_descuento(self, porcentaje):
        self.total -= self.total * (porcentaje / 100)

    def procesar_pago(self, metodo_pago):
        print(f"Procesando pago de ${self.total:.2f} por {metodo_pago}")
        return True

class SistemaPOS:
    def __init__(self, archivo_datos="datos.json"):
        self.archivo_datos = archivo_datos
        self.clientes = []
        self.productos = []
        self.ingresos_diarios = 0.0
        self.cargar_datos()

    def cargar_datos(self):
            try:
                with open(self.archivo_datos, "r") as archivo:
                    datos = json.load(archivo)
                    self.productos = [Producto(p['nombre'], p['precio'], p['stock']) for p in datos.get('productos', [])]
                    self.clientes = [Cliente(c['nombre']) for c in datos.get('clientes', [])]
                    self.ingresos_diarios = datos.get('ingresos_diarios', 0.0)
            except FileNotFoundError:
                print("No se encontró el archivo de datos. Iniciando con datos vacíos.")
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. Iniciando con datos vacíos.")

    def guardar_datos(self):
            datos = {
                'productos': [{'nombre': p.nombre, 'precio': p.precio, 'stock': p.stock} for p in self.productos],
                'clientes': [{'nombre': c.nombre} for c in self.clientes],
                'ingresos_diarios': self.ingresos_diarios
            }
            with open(self.archivo_datos, "w") as archivo:
                json.dump(datos, archivo, indent=4)
    def agregar_producto(self, nombre, precio, stock):
        producto = Producto(nombre, precio, stock)
        self.productos.append(producto)
        self.guardar_datos()


    def mostrar_menu(self):
        print("Menú de productos:")
        for producto in self.productos:
            print(producto)

    def consultar_precio(self, nombre):
        encontrado = False
        for producto in self.productos:
            if nombre.lower() in producto.nombre.lower():
                print(f'El precio de {producto.nombre} es ${producto.precio:.2f}')
                encontrado = True
        
        if not encontrado:
            print(f'Producto que contiene "{nombre}" no encontrado')
        
        return None

    def verificar_existencias(self, nombre):
        encontrado = False

        for producto in self.productos:
            if nombre.lower() in producto.nombre.lower():
                print(f'Quedan {producto.stock} unidades de {producto.nombre}')
                encontrado = True

        if not encontrado:
          print(f'Producto {nombre} no encontrado')        
        return None
    def verificar_producto(self, nombre):
        for producto in self.productos:
            if nombre.lower() in producto.nombre.lower():
              return producto

        return None
    
    def procesar_venta(self, cliente_nombre, items, descuento=0, metodo_pago="Efectivo"):
        cliente = next((c for c in self.clientes if c.nombre == cliente_nombre), None)
        if cliente is None:
            cliente = Cliente(cliente_nombre)
            self.clientes.append(cliente)

        pedido = Pedido(cliente)

        for nombre, cantidad in items:
            productos_encontrados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]

            if len(productos_encontrados) == 1:
                producto = productos_encontrados[0]
                pedido.agregar_item(producto, cantidad)
            
            elif len(productos_encontrados) > 1:
                print(f"Se encontraron varios productos para '{nombre}':")
                for i, producto in enumerate(productos_encontrados, 1):
                    print(f"{i}. {producto.nombre} - ${producto.precio:.2f}")
                
                seleccion = int(input(f"Selecciona el número del producto que deseas agregar: "))
                producto_seleccionado = productos_encontrados[seleccion - 1]
                pedido.agregar_item(producto_seleccionado, cantidad)
            
            else:
                print(f"Producto '{nombre}' no encontrado")

        if descuento > 0:
            pedido.aplicar_descuento(descuento)

        if pedido.procesar_pago(metodo_pago):
            cliente.agregar_pedido(pedido)
            self.ingresos_diarios += pedido.total
            print(f"Venta procesada exitosamente para {cliente_nombre}. Total: ${pedido.total:.2f}")
        self.guardar_datos()

    def generar_informe(self):
        print(f"Ingresos diarios: ${self.ingresos_diarios:.2f}")
        print("Ventas por cliente:")
        for cliente in self.clientes:
            print(f"{cliente.nombre}: ${cliente.total_gastado():.2f}")

def main():
    sistema = SistemaPOS()
    sistema.agregar_producto("Helado Chocolate", 25.0, 20)
    sistema.agregar_producto("Helado Vainilla", 20.0, 15)
    sistema.agregar_producto("Agua Fresa/Kiwi", 18.0, 10)
    while True:
        print("\n--- Sistema POS Heladería/Postres ---")
        print("1. Agregar producto")
        print("2. Mostrar menú de productos")
        print("3. Consultar precio de un producto")
        print("4. Verificar existencias de un producto")
        print("5. Procesar venta")
        print("6. Generar informe")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio del producto: "))
            stock = int(input("Stock disponible: "))
            sistema.agregar_producto(nombre, precio, stock)
            print(f"Producto '{nombre}' agregado exitosamente.")
        
        elif opcion == "2":
            sistema.mostrar_menu()
        
        elif opcion == "3":
            nombre = input("Nombre del producto: ")
            sistema.consultar_precio(nombre)
        
        elif opcion == "4":
            nombre = input("Nombre del producto: ")
            sistema.verificar_existencias(nombre)
        
        elif opcion == "5":
            cliente_nombre = input("Nombre del cliente: ")
            items = []
            
            while True:
                producto = input("Nombre del producto (o 'terminar' para finalizar): ")
                if producto.lower() == 'terminar':
                    break
                  
                item = sistema.verificar_producto(producto)
                cantidad = int(input(f"Cantidad de '{item.nombre}': "))
                items.append((item.nombre, cantidad))
            
            descuento = float(input("Descuento (%) a aplicar (0 si no hay): "))
            metodo_pago = input("Método de pago (Efectivo/Tarjeta): ")
            
            sistema.procesar_venta(cliente_nombre, items, descuento, metodo_pago)
            
            print("Venta procesada exitosamente.")

        
        elif opcion == "6":
            sistema.generar_informe()
        
        elif opcion == "7":
            print("Saliendo del sistema POS...")
            break
        
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
