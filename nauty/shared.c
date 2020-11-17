/* shared.c */

#include "gtools.h"
#include "gutils.h"

void writeadj(FILE *f, graph *g, int n)
{
    int d, i, j, m;
    char str[80];
    set *gv;
    m = (n + WORDSIZE - 1) / WORDSIZE;
    for (i = 0; i < n; ++i)
    {
        gv = GRAPHROW(g, i, 1);
        d = 0;
        for (j = 0; j < n; ++j)
            if (ISELEMENT(gv, j))
                ++d;
        if (d < 10)
            sprintf(str, " %d", d);
        sprintf(str, "%d", d);
        for (j = 0; j < n; ++j)
        {
            if (j)
                fwrite(" ", 1, 1, f);
            if (i == j)
            {
                fwrite(" ", 1, 1, f);
                fwrite(str, 1, strlen(str), f);
            }
            else if (ISELEMENT(gv, j))
                fwrite("-1", 1, 2, f);
            else fwrite(" 0", 1, 2, f);
        }
        fwrite("\n", 1, 1, f);
    }
    fwrite("\n", 1, 1, f);
}

/************************************************************************/

void writepg(FILE *f, graph *g, int n)
{
    int d, i, j, m;
    char str[80];
    set *gv;
    m = (n + WORDSIZE - 1) / WORDSIZE;
    fwrite("{", 1, 1, f);
    for (i = 0; i < n; ++i)
    {
        if (i)
            fwrite(", ", 1, 2, f);
        sprintf(str, "%d: {", i);
        fwrite(str, 1, strlen(str), f);
        gv = GRAPHROW(g, i, 1);
        d = 0;
        for (j = 0; j < n; ++j)
        {
            if (ISELEMENT(gv,j))
            {
                if (d++)
                    fwrite(", ", 1, 2, f);
                sprintf(str, "%d: 1", j);
                fwrite(str, 1, strlen(str), f);
            }
        }
        fwrite("}", 1, 1, f);
    }
    fwrite("}\n", 1, 2, f);
}

/************************************************************************/

void writetkz(FILE *f, graph *g, int n)
{
    int d, i, j, m;
    char str[80];
    set *gv;
    m = (n + WORDSIZE - 1) / WORDSIZE;
    sprintf(str, "\\begin{tikzpicture}\n");
    fwrite(str, 1, strlen(str), f);
    sprintf(str, "  \\GraphInit[vstyle=Art]\n");
    fwrite(str, 1, strlen(str), f);
    sprintf(str, "  \\grEmptyCycle[prefix=a,RA=2]{%d}\n", n);
    fwrite(str, 1, strlen(str), f);
    for (i = 0; i < n; ++i)
    {
        gv = GRAPHROW(g, i, 1);
        for (j = 0; j < n; ++j)
            if (ISELEMENT(gv,j))
            {
                sprintf(str, "  \\Edge(a%d)(a%d)\n", i, j);
                fwrite(str, 1, strlen(str), f);
            }
    }
    sprintf(str, "\\end{tikzpicture}\n\n");
    fwrite(str, 1, strlen(str), f);
}

/**************************************************************************/

typedef struct combinations
{
    int n, t, c[MAXN + 1];
} combinations;

/**************************************************************************/

int combinations_init(combinations *c)
{
    int j;
    for (j = 0; j < c->t; ++j)
        c->c[j] = j;
    c->c[c->t] = c->n;
}

/**************************************************************************/

int combinations_next(combinations *c)
{
    int j = 1;
    //  R3
    if (c->t & 1)
    {
        if (c->c[0] + 1 < c->c[1])
        {
            c->c[0] = c->c[0] + 1;
            return 1;
        }
        else goto R4;
    }
    else
    {
        if (c->c[0])
        {
            c->c[0] = c->c[0] - 1;
            return 1;
        }
        else goto R5;
    }
    R4:  //  R4
    if (j == c->t)
        return 0;
    if (c->c[j] > j)
    {
        c->c[j] = c->c[j - 1];
        c->c[j - 1] = j - 1;
        return 1;
    }
    ++j;
    R5:  //  R5
    if (j == c->t)
        return 0;
    if (c->c[j] + 1 < c->c[j + 1])
    {
        c->c[j - 1] = c->c[j];
        c->c[j] = c->c[j] + 1;
        return 1;
    }
    ++j;
    goto R4;
}

/**************************************************************************/

boolean degree_sequence_match(graph *g, int m, int n)
{
    int i, j, v1, v2, *d;
    set *s;
    d = malloc(n * sizeof(int));
    memset(d, 0, n * sizeof(int));
    for (i = 0; i < n; ++i)
        d[i] = 0;
    for (i = 0; i < n; ++i)
    {
        v1 = v2 = 0;
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                continue;
            else if (ISELEMENT(s, j))
                ++v1;
            else ++v2;
        ++d[v1];
        --d[v2];
    }
    for (i = 0; i < n; ++i)
        if (d[i])
        {
            free(d);
            return FALSE;
        }
    free(d);
    return TRUE;
}

/**************************************************************************/

boolean floyd_warshall(int *a, int n)
{
    int i, j, k, *a_i, *a_k;
    for (k = 0, a_k = a; k < n; ++k, a_k += n)
        for (i = 0, a_i = a; i < n; ++i, a_i += n)
            for (j = 0; j < n; ++j)
                if (*(a_i + j) > *(a_i + k) + *(a_k + j))
                    *(a_i + j) = *(a_i + k) + *(a_k + j);
    return TRUE;
}

/**************************************************************************/

boolean distance_hereditary(graph *g, int m, int n)
{
    int i, j, u, v, w, x, d1, d2, d3, infinity, *a_i, *a_u, *a_v, *a_w, *a;
    set *s;
    infinity = 1000000;
    a = malloc(n * n * sizeof(int));
    memset(a, 0, n * n * sizeof(int));
    for (i = 0, a_i = a; i < n; ++i, a_i +=n)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                *(a_i + j) = 0;
            else if (ISELEMENT(s, j))
                *(a_i + j) = 1;
            else *(a_i + j) = infinity;
    }
    floyd_warshall(a, n);
    for (u = 0, a_u = a; u < n; ++u, a_u += n)
        for (v = u + 1, a_v = a_u + n; v < n; ++v, a_v += n)
            for (w = v + 1, a_w = a_v + n; w < n; ++w, a_w += n)
                for (x = w + 1; x < n; ++x)
                {
                    d1 = *(a_u + v) + *(a_w + x);
                    d2 = *(a_u + w) + *(a_v + x);
                    d3 = *(a_u + x) + *(a_v + w);
                    if (d1 != d2 && d1 != d3 && d2 != d3)
                    {
                        free(a);
                        return FALSE;
                    }
                }
    free(a);
    return TRUE;
}

/**************************************************************************/

boolean distance_preserving(graph *g, int m, int n)
{
    int i, j, t, infinity, sum, *a_i, *b_i, *a, *b;
    set *s;
    combinations *c;
    c = malloc(sizeof(combinations)); 
    c->n = n;
    infinity = 1000000;
    a = malloc(n * n * sizeof(int));
    memset(a, 0, n * n * sizeof(int));
    for (i = 0, a_i = a; i < n; ++i, a_i +=n)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                *(a_i + j) = 0;
            else if (ISELEMENT(s, j))
                *(a_i + j) = 1;
            else *(a_i + j) = infinity;
    }
    floyd_warshall(a, n);
    for (t = n; t; --t)
    {
        b = malloc(t * t * sizeof(int));
        b = memset(b, 0, t * t * sizeof(int));
        c->t = t;
        combinations_init(c);
        do
        {
            for (i = 0, b_i = b; i < t; ++i, b_i += t)
            {
                s = GRAPHROW(g, c->c[i], m);
                for (j = 0; j < t; ++j)
                    if (i == j)
                        *(b_i + j) = 0;
                    else if (ISELEMENT(s, c->c[j]))
                        *(b_i + j) = 1;
                    else *(b_i + j) = infinity;
            }
            floyd_warshall(b, t);
            for (i = 0, b_i = b; i < t; ++i, b_i += t)
            {
                a_i = a + c->c[i] * n;
                for (j = 0; j < t; ++j)
                    if (*(b_i + j) != *(a_i + c->c[j]))
                        goto NOT_DP_SUBGRAPH;
            }
            goto DP_SUBGRAPH;
            NOT_DP_SUBGRAPH:
            ;
        }
        while (combinations_next(c));
        free(b);
        return FALSE;
        DP_SUBGRAPH:
        free(b);
    }
    free(a);
    free(c);
	return TRUE;
}

/*boolean distance_preserving(graph *g, int m, int n)
{
    int i, j, k, l, infinity, sum, is_dp_subgraph,
        *a_i, *a_j, *b_j, *a, *b, *v, *has_dp_subgraph;
    set *s;
    if (distance_hereditary(g, m, n))
        return TRUE;
    infinity = 1000000;
    v = malloc(n * sizeof(int));
    a = malloc(n * n * sizeof(int));
    memset(a, 0, n * n * sizeof(int));
    for (i = 0, a_i = a; i < n; ++i, a_i +=n)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                *(a_i + j) = 0;
            else if (ISELEMENT(s, j))
                *(a_i + j) = 1;
            else *(a_i + j) = infinity;
    }
    floyd_warshall(a, n);
    has_dp_subgraph = malloc(n * sizeof(int));
    memset(has_dp_subgraph, 0, n * sizeof(int));
    for (i = 1; i < 1 << n; ++i)
    {
        is_dp_subgraph = 1;
        k = 0;
        memset(v, 0, n * sizeof(int));
        for (j = 0; j < n; ++j)
            if ((i >> j) % 2 == 1)
                v[k++] = j;
        if (has_dp_subgraph[k - 1])
            continue;
        b = malloc(k * k * sizeof(int));
        b = memset(b, 0, k * k * sizeof(int));
        for (j = 0, b_j = b; j < k; ++j, b_j += k)
        {
            s = GRAPHROW(g, v[j], m);
            for (l = 0; l < k; ++l)
                if (j == l)
                    *(b_j + l) = 0;
                else if (ISELEMENT(s, v[l]))
                    *(b_j + l) = 1;
                else *(b_j + l) = infinity;
        }
        floyd_warshall(b, k);
        is_dp_subgraph = 1;
        for (j = 0, b_j = b; j < k; ++j, b_j += k)
        {
            a_j = a + v[j] * n;
            for (l = 0; l < k; ++l)
                if (*(b_j + l) != *(a_j + v[l]))
                    is_dp_subgraph = 0;
        }
        if (is_dp_subgraph)
            has_dp_subgraph[k - 1] = 1;
        free(b);
    }
    sum = 0;
    for (i = 0; i < n; ++i)
        if (has_dp_subgraph[i])
            ++sum;
    free(a);
    free(v);
    free(has_dp_subgraph);
    if (sum == n)
        return TRUE;
	return FALSE;
}*/

/**************************************************************************/

int induced_cycle(graph *g, int m, int n)
{
    int i, j, t, m2, maxc, maxd, minc, mind;
    boolean eul;
    unsigned long e;
    graph g2[MAXN*MAXM];
    set *s, *s2;
    combinations *c;
    c = malloc(sizeof(combinations)); 
    c->n = n;
    for (t = n; t; --t)
    {
        c->t = t;
        combinations_init(c);
        m2 = (t + WORDSIZE - 1) / WORDSIZE;
        do
        {
            for (i = 0; i < m2 * t; ++i)
                g2[i] = 0;
            for (i = 0; i < t; ++i)
            {
                s = GRAPHROW(g, c->c[i], m);
                s2 = GRAPHROW(g2, i, m2);
                for (j = 0; j < t; ++j)
                    if (ISELEMENT(s, c->c[j]))
                        ADDELEMENT(s2, j);
            }
            if (isconnected(g2, m2, t))
            {
                degstats(g2, m2, t, &e, &mind, &minc, &maxd, &maxc, &eul);
                if (mind == 2 && maxd == 2)
                {
                    free(c);
                    return t;
                }
            }
        }
        while (combinations_next(c));
    }
    free(c);
    return 0;
}

/*int induced_cycle(graph *g, int m, int n)
{
    int i, j, k, m2, n2, cycle, maxc, maxd, minc, mind, *v;
    boolean eul;
    unsigned long e;
    graph g2[MAXN*MAXM];
    set *s, *s2;
    v = malloc(n * sizeof(int));
    memset(v, 0, n * sizeof(int));
    cycle = 0;
    for (k = 1; k < 1 << n; ++k)
    {
        n2 = 0;
        for (i = 0; i < n; ++i)
            if ((k >> i) % 2)
                v[n2++] = i;
        if (n2 <= cycle)
            continue;
	    m2 = (n2 + WORDSIZE - 1) / WORDSIZE;
	    for (i = 0; i < m2 * n2; ++i)
            g2[i] = 0;
        for (i = 0; i < n2; ++i)
        {
            s = GRAPHROW(g, v[i], m);
            s2 = GRAPHROW(g2, i, m2);
            for (j = 0; j < n2; ++j)
                if (ISELEMENT(s, v[j]))
                    ADDELEMENT(s2, j);
        }
        if (isconnected(g2, m2, n2))
        {
            degstats(g2, m2, n2, &e, &mind, &minc, &maxd, &maxc, &eul);
            if (mind == 2 && maxd == 2 && n2 > cycle)
                cycle = n2;
        }
    }
    free(v);
    return cycle;
}*/

/**************************************************************************/

boolean distance_list_match(graph *g, int m, int n)
{
    int i, j, k, infinity, *a_i, *a_j, *a_k, *a1, *a2, *d;
    set *s;
    infinity = 1000000;
    a1 = malloc(n * n * sizeof(int));
    memset(a1, 0, n * n * sizeof(int));
    a2 = malloc(n * n * sizeof(int));
    memset(a2, 0, n * n * sizeof(int));
    d = malloc(n * sizeof(int));
    memset(d, 0, n * sizeof(int));
    for (i = 0, a_i = a1; i < n; ++i, a_i +=n)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                *(a_i + j) = 0;
            else if (ISELEMENT(s, j))
                *(a_i + j) = 1;
            else *(a_i + j) = infinity;
    }
    for (i = 0, a_i = a2; i < n; ++i, a_i +=n)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (i == j)
                *(a_i + j) = 0;
            else if (ISELEMENT(s, j))
                *(a_i + j) = infinity;
            else *(a_i + j) = 1;
    }
    floyd_warshall(a1, n);
    floyd_warshall(a2, n);
    for (i = 0, a_i = a1; i < n; ++i, a_i += n)
        for (j = i + 1; j < n; ++j)
            if (*(a_i + j) != infinity)
                ++d[*(a_i + j)];
    for (i = 0, a_i = a2; i < n; ++i, a_i += n)
        for (j = i + 1; j < n; ++j)
            if (*(a_i + j) != infinity)
                --d[*(a_i + j)];
    free(a1);
    free(a2);
    for (i = 0; i < n; ++i)
        if (d[i])
        {
            free(d);
            return FALSE;
        }
    free(d);
    return TRUE;
}

/**************************************************************************/

boolean lu_decomposition(double *a, int n)
{
    int i, j, k;
    double *a_i, *a_j, *a_k;
    for (k = 0, a_k = a; k < n; ++k, a_k += n)
    {
        for (i = k; i < n; ++i)
            for (j = 0, a_j = a; j < k; ++j, a_j += n)
                *(a_k + i) -= *(a_k + j) * *(a_j + i);
        if (*(a_k + k) == 0.0)
            return FALSE;
        for (i = k + 1, a_i = a_k + n; i < n; ++i, a_i += n)
        {
            for (j = 0, a_j = a; j < k; ++j, a_j += n)
                *(a_i + k) -= *(a_i + j) * *(a_j + k);
            *(a_i + k) /= *(a_k + k);
        }
    }
    return TRUE;
}

/**************************************************************************/

long long spanning_tree_count(graph *g, int m, int n)
{
    int i, j;
    double *a_i, *a;
    long double det;
    set *s;
    a = malloc((n - 1) * (n - 1) * sizeof(double));
    memset(a, 0, (n - 1) * (n - 1) * sizeof(double));
    for (i = 0, a_i = a; i < n - 1; ++i, a_i += n - 1)
    {
        s = GRAPHROW(g, i, m);
        for (j = 0; j < n; ++j)
            if (ISELEMENT(s, j))
            {
                ++*(a_i + i);
                if (j < n - 1)
                    *(a_i + j) = -1;
            }
    }
    if (!lu_decomposition(a, n - 1))
        return 0;
    det = 1;
    for (i = 0, a_i = a; i < n - 1; ++i, a_i += n)
        det *= *a_i;
    free(a);
    return (long long) (det + .5);
}
