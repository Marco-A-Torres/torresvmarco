<html>
  <head>
   <title> Ejemplo de operadores logicos </title>
  </head>
  <body>
    <h1>Ejemplo de operaciones logicas en PHP </h1>
    <?php
      $a=8;
      $b=3;
      $c=3;
      echo ($a==$b)&&($c>$b), "<br>";
      echo ($a==$b)||($b==$c), "<br>";
      echo !($b<=$c), "<br>";
      
     ?>
    
  </body>
</html>