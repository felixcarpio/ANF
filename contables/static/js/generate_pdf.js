$(document).ready(function(){
  var specialElementHandlers={
    "#editor":function(element,renderer){
      return true;
    }
  };

    $("#pdf").click(function(){
      var doc = new jsPDF();
      doc.fromHTML($("#contenidoPDF").html(),15,15,{
        "width":170,
        "elementHandlers":specialElementHandlers
      });

      doc.save("Comparacion-Cuentas.pdf");
    });
});
