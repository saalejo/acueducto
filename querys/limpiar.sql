-- SQLite
delete from util_control;
delete from util_subsidio;
delete from util_consumo;
delete from util_movimiento;

-- PostgreSQL
TRUNCATE util_control, util_subsidio, util_consumo, util_movimiento;