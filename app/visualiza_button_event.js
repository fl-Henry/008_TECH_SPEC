function() {
  var obj = g_globalObject.getSelectedDay();
  var a = 0,
    rdbtn = document.getElementsByName("capital");
  for (i = 0; i < rdbtn.length; i++) {

    if (rdbtn.item(i).checked == true) {
      var selec3 = rdbtn.item(i).value;
      if ((obj.day != null) && selec3 != null) {
        var di = parseInt(obj.day, 10);
        var me = parseInt(obj.month, 10);

        if ((di <= "31") && (me <= "12") && (obj.year >= "2017")) {
          if (me <= "9" && obj.year == "2017") {
            //if ((di<"27")){
            if (obj.year == "2017") {
              if ((me == "9") && (di > "26")) {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec3 + "pdf", "_blank");
                break;
              } else {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec3 + "swf", "_blank");

                break;
              }

            }

          }
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec3 + "pdf", "_blank");

        } else {
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec3 + "swf", "_blank");
        }
        //	if((di>"26") && (me>="9") && (obj.year>="2017") ){
        //alert(di);
        //		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec3+"pdf", "_blank");
        //	}

        //	else{

        //alert(di);
        //		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec3+"swf", "_blank");
        //		}

        break;
      }
    }
  }




  var a1 = 0,
    rdbtn1 = document.getElementsByName("GomezLerdo");
  for (i = 0; i < rdbtn1.length; i++) {
    if (rdbtn1.item(i).checked == true) {
      var selec = rdbtn1.item(i).value;
      if ((obj.day != null) && selec != null) {
        var di = parseInt(obj.day, 10);
        var me = parseInt(obj.month, 10);
        //window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec, "_blank");
        /*if((di>"26") && (me>="9") && (obj.year>="2017") ){
        		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec+"pdf", "_blank");
        		}
        		else{
        		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec+"swf", "_blank");
        		}*/
        if ((di <= "31") && (me <= "12") && (obj.year >= "2017")) {
          if (me <= "9" && obj.year == "2017") {
            //if ((di<"27")){
            if (obj.year == "2017") {
              if ((me == "9") && (di > "26")) {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec + "pdf", "_blank");
                break;
              } else {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec + "swf", "_blank");

                break;
              }

            }

          }
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec + "pdf", "_blank");

        } else {
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec + "swf", "_blank");
        }
      }

      break;
    }
  }




  var a2 = 0,
    rdbtn2 = document.getElementsByName("Foraneo");
  for (i = 0; i < rdbtn2.length; i++) {
    if (rdbtn2.item(i).checked == true) {
      var selec2 = rdbtn2.item(i).value;
      if ((obj.day != null) && selec2 != null) {
        var di = parseInt(obj.day, 10);
        var me = parseInt(obj.month, 10);
        //window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec2, "_blank");
        /*if((di>"26") && (me>="9") && (obj.year>="2017") ){
        		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec2+"pdf", "_blank");
        		}
        		else{
        		window.open("images/flash/ListasAcuerdos/"+di+me+obj.year+"/"+selec2+"swf", "_blank");
        		}*/
        if ((di <= "31") && (me <= "12") && (obj.year >= "2017")) {
          if (me <= "9" && obj.year == "2017") {
            //if ((di<"27")){
            if (obj.year == "2017") {
              if ((me == "9") && (di > "26")) {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec2 + "pdf", "_blank");
                break;
              } else {
                window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec2 + "swf", "_blank");

                break;
              }

            }

          }
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec2 + "pdf", "_blank");

        } else {
          window.open("images/flash/ListasAcuerdos/" + di + me + obj.year + "/" + selec2 + "swf", "_blank");
        }
      }
      break;

    }
  }
}

