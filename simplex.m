function [z,x] = simplex(M)
  while(true)
    M
    custos = M(1,:);
    z = -1*custos(length(custos));
    x = getX(M,custos);
    if(custos>=0)
      break;
    endif
    [x_i,index_x_i] = min(custos);
    aux = M(:,columns(M))./M(:,index_x_i);
    aux(1) = [];
    for(i= 1:length(aux))
      if(aux(i) <= 0)
        aux(i) = Inf;
      endif
    endfor
    [y_i,index_y_i] = min(aux);
    M = pivoteamento_gaussiano(index_y_i+1,index_x_i,M);
  endwhile
endfunction

function M = pivoteamento_gaussiano(row,column,M)
  pivo = M(row,column);
  for(i = 1:rows(M))
    if(i != row)
      M(i,:) = M(i,:) - (M(i,column)/pivo).*M(row,:);
    endif
  endfor
  M(row,:) = M(row,:)./pivo;
endfunction

function x = getX(M,custos)
  for i=1:length(custos)-1
    if(custos(i) != 0)
      x(i) = 0;
    else
      row = M(:,i);
      for j = 2:length(row)
        if(row(j) != 0)
          x(i) = M(j,columns(M));
          break;
        endif
      endfor
    endif
  endfor
endfunction
