<html>
<head>
<tille>Tabla condicional</title>
</head>
<body>
<h1>Tabla condicional </h1>
<?php
/* Crearemos una tabla de valores de seno y coseno de O a 2
"enincrementos de 0.01.Los valores negativos que resultenlos queremos mostrar en rojo,y los valores positivos en azul */
/* En primer lugar vamos a crear una funcion con las condicionales
Aqui estamos usando la sentencion de FUNCTION alquele pasamos un valor
dependiendo de este valor,ejecutamos una condicion IF..ELSE...  y asignamos un color altipo de letra para generar la tabla */
function muestra($valor)
 { 
if ($valor < 0.5)
$color = "red";
else
$color = "blue";
echo "<td><font color='$color'>$valor</font></td>\n";
}
?>
<table border="l">
<?php
for ($x=O;$x<=2;$x+=0.01){
echo "<tr>";
muestra($x); 
muestra(sin($x)); 
muestra(cos($x));
echo "</tr>";
}
?>
</body>
</html>