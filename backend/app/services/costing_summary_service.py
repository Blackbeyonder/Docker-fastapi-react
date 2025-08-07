from sqlalchemy.orm import Session
from app.models.costing_summary import CostingSummary
from app.models.costing import CostRecord
from app.models.shipment import Shipment
from typing import Optional

class CostingSummaryService:
    """
    Servicio para manejar la lógica de negocio de CostingSummary
    """
    
    @staticmethod
    def create_summary_from_shipment(db: Session, shipment_id: int) -> Optional[CostingSummary]:
        """
        Crea un resumen de costos cuando un shipment se marca como FINALIZADO
        """
        print(f"[DEBUG] Starting create_summary_from_shipment for shipment_id: {shipment_id}")
        
        # Obtener el shipment
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            print(f"[DEBUG] Shipment {shipment_id} not found")
            return None
        
        print(f"[DEBUG] Found shipment: {shipment.reference}, status: {shipment.status}")
        
        # Verificar que no exista ya un resumen para este viaje
        existing_summary = db.query(CostingSummary).filter(
            CostingSummary.viaje == shipment.reference
        ).first()
        
        if existing_summary:
            print(f"[DEBUG] Existing summary found for viaje: {shipment.reference}")
            return existing_summary
        
        # Obtener todos los cost_records para este shipment
        cost_records = db.query(CostRecord).filter(
            CostRecord.shipment_id == shipment_id
        ).all()
        
        print(f"[DEBUG] Found {len(cost_records)} cost_records for shipment {shipment_id}")
        
        # Consolidar los costos por concepto
        flete = 0.0
        maniobra = 0.0
        estadias = 0.0
        devoluciones = 0.0
        otros = 0.0
        
        # Si hay cost_records, procesarlos
        if cost_records:
            for record in cost_records:
                concepto = record.concepto.upper()
                print(f"[DEBUG] Processing cost record: concepto='{record.concepto}', costo={record.costo}")
                if "FLETE" in concepto:
                    flete += record.costo
                elif "MANIOBRA" in concepto:
                    maniobra += record.costo
                elif "ESTADIA" in concepto or "ESTADÍAS" in concepto:
                    estadias += record.costo
                elif "DEVOLUCION" in concepto or "DEVOLUCIÓN" in concepto:
                    devoluciones += record.costo
                else:
                    otros += record.costo
        else:
            print(f"[DEBUG] No cost_records found for shipment {shipment_id} - will create summary with zero values")
        
        print(f"[DEBUG] Consolidated costs - flete: {flete}, maniobra: {maniobra}, estadias: {estadias}, devoluciones: {devoluciones}, otros: {otros}")
        
        # Crear el resumen de costos
        try:
            summary = CostingSummary(
                viaje=shipment.reference,
                shipment_id=shipment_id,
                flete=flete,
                maniobra=maniobra,
                estadias=estadias,
                devoluciones=devoluciones,
                otros=otros,
                validado=False
            )
            
            print(f"[DEBUG] Created CostingSummary object: viaje={summary.viaje}, shipment_id={summary.shipment_id}")
            
            db.add(summary)
            db.commit()
            db.refresh(summary)
            
            print(f"[DEBUG] Successfully saved CostingSummary with ID: {summary.id}")
            return summary
            
        except Exception as e:
            print(f"[ERROR] Failed to create CostingSummary: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    def dispatch_to_sabanas(db: Session, summary_id: int) -> bool:
        """
        Dispara información a las tablas sabana_compra y sabana_venta
        cuando se valida un resumen de costos
        """
        # TODO: Implementar la lógica para disparar a sábanas
        # Por ahora solo retornamos True como placeholder
        return True 