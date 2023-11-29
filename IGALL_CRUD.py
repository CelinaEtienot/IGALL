#-------------------------------------------------
#    definicion clase biblioteca
#-------------------------------------------------
class Biblioteca:
    def __init__(self):
        self.documentos = []

    def agregar_documento(self, codigo, titulo, area, url, last_valid_version, igall_owner):
        self.documentos.append({
            'codigo': codigo,
            'titulo': titulo,
            'Area': area,
            'url': url,
            'Last valid version': last_valid_version,
            'Igall Owner': igall_owner
        })

    def eliminar_documento(self, codigo):
        for documento in self.documentos:
            if documento['codigo'] == codigo:
                self.documentos.remove(documento)
                break

    def buscar_documento(self, codigo):
        for documento in self.documentos:
            if documento['codigo'] == codigo:
                return documento
        return None

    def modificar_documento(self, codigo, titulo, area, url, last_valid_version, igall_owner):
        for documento in self.documentos:
            if documento['codigo'] == codigo:
                documento['titulo'] = titulo
                documento['Area'] = area
                documento['url'] = url
                documento['Last valid version'] = last_valid_version
                documento['Igall Owner'] = igall_owner
                break

    def listar_documentos(self):
        print("-" * 50)
        for documento in self.documentos:
            print(f"Código.....: {documento['codigo']}")
            print(f"Título.....: {documento['titulo']}")
            print(f"Área.......: {documento['Area']}")
            print(f"URL........: {documento['url']}")
            print(f"Última versión válida: {documento['Last valid version']}")
            print(f"Propietario: {documento['Igall Owner']}")
            print("-" * 50)

#-------------------------------------------------
#    definicion clase AMR
#-------------------------------------------------
class AMR:
    def __init__(self):
        self.lineas = []

    def agregar_linea(self, table_no, igall_no, system, structure_component, critical_location_part, material, environment, ageing_effect, degradation_mechanism, amp, design):
        self.lineas.append({
            'Table No#': table_no,
            'IGALL No#': igall_no,
            'System': system,
            'Structure_component': structure_component,
            'Critical_location_part': critical_location_part,
            'Material': material,
            'Environment': environment,
            'Ageing_Effect': ageing_effect,
            'Degradation_mechanism': degradation_mechanism,
            'AMP': amp,
            'Design': design
        })

    def eliminar_linea(self, table_no):
        for linea in self.lineas:
            if linea['Table No#'] == table_no:
                self.lineas.remove(linea)
                break

    def buscar_linea(self, table_no):
        for linea in self.lineas:
            if linea['Table No#'] == table_no:
                return linea
        return None

    def modificar_linea(self, table_no, igall_no, system, structure_component, critical_location_part, material, environment, ageing_effect, degradation_mechanism, amp, design):
        for linea in self.lineas:
            if linea['Table No#'] == table_no:
                linea['IGALL No#'] = igall_no
                linea['System'] = system
                linea['Structure_component'] = structure_component
                linea['Critical_location_part'] = critical_location_part
                linea['Material'] = material
                linea['Environment'] = environment
                linea['Ageing_Effect'] = ageing_effect
                linea['Degradation_mechanism'] = degradation_mechanism
                linea['AMP'] = amp
                linea['Design'] = design
                break

    def listar_lineas(self):
        print("-" * 50)
        for linea in self.lineas:
            print(f"Table No#...............: {linea['Table No#']}")
            print(f"IGALL No#...............: {linea['IGALL No#']}")
            print(f"System..................: {linea['System']}")
            print(f"Structure_component.....: {linea['Structure_component']}")
            print(f"Critical_location_part..: {linea['Critical_location_part']}")
            print(f"Material................: {linea['Material']}")
            print(f"Environment.............: {linea['Environment']}")
            print(f"Ageing_Effect...........: {linea['Ageing_Effect']}")
            print(f"Degradation_mechanism....: {linea['Degradation_mechanism']}")
            print(f"AMP.....................: {linea['AMP']}")
            print(f"Design..................: {linea['Design']}")
            print("-" * 50)
