<html>
  <head>
    <title>Tabla condicional2</title>
  </head>
  <body>
<h1>Tabla condicional 2</hl>
<?php
/* Crearemos una tabla de valores de seno y coseno de O a 2
enincrementos de 0.01.Los valores negativos que resultenlos queremos
"mostrar en rojo,y los valores positivos en azul */

/* Variacion. Un color diferente cada fila que se imprima */
function  muestra($valor)  
{ 
if ($renglon % 2)
	$fondo = "#eeeeee"; 
else
	$fondo = "#dddddd";
if ($valor < 0.5)
	$color = "red";
else
    $color = "blue";


  echo "<td bgcolor='$fondo'><font color='$color'>$valor</font></td>\n";
}
?>
<table border="1">
<?php
$nrenglon = 0;
for ($x=0; $x<=2; $x+=0.01)
{
echo "<tr>";
muestra($x); 
muestra(sin($x)); 
muestra(cos($x));
echo "</tr>";
}
?>
  </body>
</html>     