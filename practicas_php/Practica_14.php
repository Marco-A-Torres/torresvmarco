<html>
<head>
<title>Calculos </title>
</head>
<body>
<h1>Calculos,redondeo y formato.</hl>"
<?php
/* Primero declaramos las variables*/
$precioneto = 101.98;
$iva = 0.196;
$resultado = $precioneto * $iva; 
echo "Elprecio es de ";
echo $precioneto; 
echo " y el IVA él "; 
echo $iva;
echo "%<br>";
echo "Resultado:" ;
echo round($resultado,2)," ";
echo " con ROUND() <br>"; 
echo $resultado;
echo " normal \n";
echo "<br><br>";
$resultado2    =   sprintf("%01.2f",$resultado);
echo "Usandola funcion PRINTF se ve asi:"; 
echo  $resultado2;
?>
</body>
</html>