## Gradient Descents

### Gradient
Основное свойство антиградиента &ndash; он указывает в сторону наискорейшего убывания функции в данной точке. Соответственно, будет логично стартовать из некоторой точки, сдвинуться в сторону антиградиента, пересчитать антиградиент и снова сдвинуться в его сторону и т.д. Запишем это более формально.

Пусть $w_0$ &ndash; начальный набор параметров (например, нулевой или сгенерированный из некоторого случайного распределения). Тогда ванильный градиентный спуск состоит в повторении следующих шагов до сходимости:
$$
    w_{k + 1} = w_{k} - \eta_{k} \nabla_{w} Q(w_{k}).
$$

Во всех методах градиентного спуска мы будем использовать следующую формулу для длины шага:  
$$
        \eta_{k} = \lambda \left(\dfrac{s_0}{s_0 + k}\right)^p
$$
Также длину шагу можно задавать константой: 
$$\eta_{k} = \eta_{0}$$

Как правило, в задачах машинного обучения функционал $Q(w)$ представим в виде суммы $\ell$ функций:    
$$
    Q(w) = \frac{1}{\ell} \sum_{i = 1}^{\ell} q_i(w).
$$

Проблема метода градиентного спуска состоит в том, что на каждом шаге необходимо вычислять градиент всей суммы:
  
   $$
      \nabla_w Q(w) = \frac{1}{\ell}\sum_{i = 1}^{\ell}\nabla_w q_i(w).
    $$

### Stochastic Gradient Descent
Оценить градиент суммы функций можно средним градиентов случайно взятого подмножества функций:
  
   $$
   \nabla_{w} Q(w_{k}) \approx \dfrac{1}{|B|}\sum\limits_{i \in B}\nabla_{w} q_{i}(w_{k}),
    $$
    где $B$ - это случайно выбранное подмножество индексов.
    
Шаг оптимизации:
$$
   w_{k + 1} = w_{k} - \eta_{k} \dfrac{1}{|B|}\sum\limits_{i \in B}\nabla_{w} q_{i}(w_{k}).
 $$

### Momentum method
Может оказаться, что направление антиградиента сильно меняется от шага к шагу. Например, если линии уровня функционала сильно вытянуты, то из-за ортогональности градиента линиям уровня он будет менять направление на почти противоположное на каждом шаге. Такие осцилляции будут вносить сильный шум в движение, и процесс оптимизации займёт много итераций. Чтобы избежать этого, можно усреднять векторы антиградиента с нескольких предыдущих шагов – в этом случае шум уменьшится, и такой средний вектор будет указывать в сторону общего направления движения. Введём для этого вектор инерции:
$$
    h_0 = 0 \\
    h_{k + 1} = \alpha h_{k} + \eta_k \nabla_w Q(w_{k})
$$
Здесь $\alpha$ &ndash; параметр метода, определяющей скорость затухания градиентов с предыдущих шагов. Разумеется, вместо вектора градиента может быть использована его аппроксимация. Чтобы сделать шаг градиентного спуска, просто сдвинем предыдущую точку на вектор инерции:
  $$
    w_{k + 1} = w_{k} - h_{k + 1}.
    $$
   
Заметим, что если по какой-то координате градиент постоянно меняет знак, то в результате усреднения градиентов в векторе инерции эта координата окажется близкой к нулю. Если же по координате знак градиента всегда одинаковый, то величина соответствующей координаты в векторе инерции будет большой, и мы будем делать большие шаги в соответствующем направлении.

### Adaptive Learning Rate
 Градиентный спуск очень чувствителен к выбору длины шага. Если шаг большой, то есть риск, что мы будем перескакивать через точку минимума; если же шаг маленький, то для нахождения минимума потребуется много итераций. При этом нет способов заранее определить правильный размер шага &ndash; к тому же, схемы с постепенным уменьшением шага по мере итераций могут тоже плохо работать.
   
В методе _AdaGrad_ предлагается сделать свою длину шага для каждой компоненты вектора параметров. При этом шаг будет тем меньше, чем более длинные шаги мы делали на предыдущих итерациях:
    
   $$
    G_{kj} = G_{k-1,j} + (\nabla_w Q(w_{k - 1}))_j^2 \\
    w_{jk} = w_{j,k-1} - \frac{\eta_t}{\sqrt{G_{kj}} + \varepsilon} (\nabla_w Q(w_{k - 1}))_j.
    $$
  
  Здесь $\varepsilon$ небольшая константа, которая предотвращает деление на ноль.
Данный метод подходит для разреженных задач, в которых у каждого объекта большинство признаков равны нулю. Для признаков, у которых ненулевые значения встречаются редко, будут делаться большие шаги; если же какой-то признак часто является ненулевым, то шаги по нему будут небольшими.
   
У метода _AdaGrad_ есть большой недостаток: переменная $G_{kj}$ монотонно растёт, из-за чего шаги становятся всё медленнее и могут остановиться ещё до того, как достигнут минимум функционала. Проблема решается в методе _RMSprop_, где используется экспоненциальное затухание градиентов:
  $$
     G_{kj} = \alpha G_{k-1,j} + (1 - \alpha) (\nabla_w Q(w^{(k-1)}))_j^2.
  $$
   В этом случае размер шага по координате зависит в основном от того, насколько быстро мы двигались по ней на последних итерациях.

### Adam
Можно объединить идеи описанных выше методов: накапливать градиенты со всех прошлых шагов для избежания осцилляций и делать адаптивную длину шага по каждому параметру.
    $$
    m_0 = 0, \quad v_0 = 0 \\
    m_{k + 1} = \beta_1 m_k + (1 - \beta_1) \nabla_w Q(w_{k}) \\
    v_{k + 1} = \beta_2 v_k + (1 - \beta_2) \left(\nabla_w Q(w_{k})\right)^2$$
    
   $$\widehat{m}_{k} = \dfrac{m_k}{1 - \beta_1^{k}}, \quad \widehat{v}_{k} = \dfrac{v_k}{1 - \beta_2^{k}}\\
    w_{k + 1} = w_{k} - \dfrac{\eta_k}{\sqrt{\widehat{v}_{k + 1}} + \varepsilon} \widehat{m}_{k + 1}
    $$
    
### Регуляризация
Регуляризация - это добавка к функции потерь, которая штрафует за норму весов. Мы будем использовать $\ell_2$ регуляризацию, таким образом функция потерь приобретает следующий вид:
    $$
     Q(w) = \dfrac{1}{\ell} \sum\limits_{i=1}^{\ell} (a_w(x_i) - y_i)^2 + \dfrac{\mu}{2} \| w \|^2
    $$
