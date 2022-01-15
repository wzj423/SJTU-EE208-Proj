function advancedSearch() {
    console.log("Got it@");

    var brandsList=document.getElementsByClassName('brandSelect');
    var brands="";
    for (let index = 0; index < brandsList.length; index++) if(brandsList[index].checked){
        if(!brands) brands += brandsList[index].id;
        else brands+=','+brandsList[index].id;
    }
    console.log(brands);
    var cateList=document.getElementsByClassName('categorySelect');
    var cate="";
    for (let index = 0; index < cateList.length; index++) if(cateList[index].checked){
        if(!cate) cate += cateList[index].id;
        else cate+=','+cateList[index].id;
    }
    console.log(cate);
    var selectList=document.getElementsByClassName('attrSelect');    
    var select="";
    for (let index = 0; index < selectList.length; index++) {
        if(!select) select += '\"'+selectList[index].id+"\":\""+selectList[index].value;
        else select+='\",'+'\"'+selectList[index].id+"\":\""+selectList[index].value;
    }
    select+='\"';
    console.log(select);
    var sortwayList=document.getElementsByName('sortway');   
    var sortway='similarity';
    for (let index = 0; index < sortwayList.length; index++) if(sortwayList[index].checked){
        sortway=sortwayList[index].value;
    }     
    console.log(sortway);
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const imageFilename = urlParams.get('imageFilename') ;   
    const logoFilename = urlParams.get('logoFilename') ; 
    const keywords=urlParams.get('keywords');
    var query;
    if( keywords && keywords!='None' && keywords!='pic Search')
        query=encodeQueryData({'keywords':keywords,'brands':brands,'cate':cate,'attr':select,'sortway':sortway});
    else if (imageFilename)
        query=encodeQueryData({'imageFilename':imageFilename,'brands':brands,'cate':cate,'attr':select,'sortway':sortway});
    else
        query=encodeQueryData({'logoFilename':logoFilename,'brands':brands,'cate':cate,'attr':select,'sortway':sortway});
    console.log(query);
    

    var url=window.location.href;
    var hrf=url.substring(0, url.indexOf('?'))+'?'+query;
    console.log(hrf);
    window.location.href=hrf;
}

function encodeQueryData(data) {
    const ret = [];
    for (let d in data)
      ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    return ret.join('&');
 }