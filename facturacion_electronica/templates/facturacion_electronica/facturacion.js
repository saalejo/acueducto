export default {
    name: 'InvoiceList',
    data() {
        return {
        invoices: [
            // Aquí irían tus datos de facturas
        ]
        }
    },
    methods: {
        facturar(id) {
        // Lógica para mostrar los detalles de la factura
        console.log('Ver factura con ID:', id);
        },
        notificar(id) {
        // Lógica para invalidar la factura
        console.log('Invalidar factura con ID:', id);
        // Aquí harías una solicitud a tu backend para actualizar el estado de la factura
        }
    }
}