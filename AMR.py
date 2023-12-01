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
#-------------------------------------------------
#    conexion con base de datos
#-------------------------------------------------

