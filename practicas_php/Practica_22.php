<html>
<head>
<title></title>
</head>
<body>
<h1>Bucle While 2</h1>
<form action="Practica_22.php" method="post">
¿Cuantas veces?
<input type="text" name="number">
<input type="submit" value="Enviar">
</form>
<p>
<?php
/* Mostraremos eluso de la sentencia While y comenzamos a usar entrada delteclado mediante un 
formulario simple */
if ( isset( $_POST['number'] )) {
    $number =$_POST['number']; 
    $counter = 1;
    while ($counter <= $number) {
    echo "<b>Scounter</b>.-  Los bucles son faciles!<br>\n";
    $counter++;
    }
    echo "Se acabo \n";
    }
    ?>
    </p>
  </body>
</html>