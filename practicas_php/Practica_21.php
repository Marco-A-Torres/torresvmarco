<html>
<head>
<title> Bucle While</title>
</head>
<body>
<h1>Bucle While</h1>
<form action="Practica_21.php" method="post">
¿Cuantas veces?
<input type="text" name="number">
<input type="submit" value="Enviar">
<?php
/* Mostraremos eluso de la sentencia While y comenzamos a usar 
erada delteclado mediante un formulario simple */

if (isset( $_POST['$number'] )) {

$number =$_POST['$number'];
$counter = 1;
while ($counter <= $number) {
echo "Los bucles son faciles!<br>\n";
$counter++;
}
echo "Se acabo.\n";
}
?>
</p>
</body>
</html>