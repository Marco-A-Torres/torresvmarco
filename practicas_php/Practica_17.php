<html>
<head>
<title>CondiclonalSwitch</title>
</head>
<body>
<hl>Condiclonal Switch. Ejemplo</h1>
<?php
/*Declaramos una variable con un valor de muestra */
$posicion="arriba";
echo "La variable posicion es ",$posicion;
echo "<br>";
switch($posiclon){
case "arriba":           // Primer condicion si es arriba 
echo "La variable contiene elvalor de arriba";
break;
case "abajo":              //Segunda condiciondelsupuesto 
echo "La variable contiene el valor de abajo";
break;
default:             //Condicion por default o si no es ninguna
echo "La variable contiene otro valor distinto arriba y abajo";
}
?>
</body>
</html>