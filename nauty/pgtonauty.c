/* pgtonauty.c */

#define USAGE \
"pgtonauty [infile [outfile]]"

#define HELPTEXT \
"Convert a file of graphs from pg to nauty format.\n\n\
    -g    :  use graph6 output\n\
    -m    :  use adjacency matrix output\n\
    -p    :  use pg output\n\
    -s    :  use sparse6 output\n\
    -u    :  do not output graphs\n\
    -z    :  use tkz-berge.sty output\n\
\n"

#ifndef MAXN
#define MAXN 32
#endif

#if MAXN > 32
#error "Can't have MAXN greater than 32"
#endif

#define ONE_WORD_SETS
#include "gtools.h"

#if MAXN < 32
typedef int xword;
#else
typedef unsigned int xword;
#endif

static FILE *infile, *outfile;           /* file for output graphs */
static int BUFFER = 1024;

/**************************************************************************/
/**************************************************************************/

int main(int argc, char *argv[])
{
    int i, j, m, n, v1, v2, argnum, codetype, b;
    char *arg, sw, l[BUFFER], *infilename, *outfilename;
    boolean badargs, quiet, gswitch, mswitch, pswitch, sswitch, uswitch,
            zswitch;
    unsigned long numread, numwritten;
    graph g[MAXN*MAXM];
    set *s;

    HELP;
    badargs = quiet = gswitch = mswitch = pswitch = sswitch = uswitch
            = zswitch = FALSE;
    numread = numwritten = 0;
    infilename = outfilename = NULL;
    argnum = 0;
    for (i = 1; !badargs && i < argc; ++i)
    {
        arg = argv[i];
        if (arg[0] == '-' && arg[1] != '\0')
        {
            ++arg;
            while (*arg != '\0')
            {
                sw = *arg++;
                SWBOOLEAN('q',quiet)
                else SWBOOLEAN('g',gswitch)
                else SWBOOLEAN('m',mswitch)
                else SWBOOLEAN('p',pswitch)
                else SWBOOLEAN('s',sswitch)
                else SWBOOLEAN('u',uswitch)
                else SWBOOLEAN('z',zswitch)
                else badargs = TRUE;
            }
        }
        else
        {
            ++argnum;
            if (argnum == 1)
                infilename = arg;
            else if (argnum == 2)
                outfilename = arg;
            else badargs = TRUE;
        }
    }
    if (gswitch + mswitch + pswitch + sswitch + uswitch + zswitch > 1)
        gt_abort(">E nautytopg: -gmpsuz are incompatible\n");
    if (badargs)
    {
        fprintf(stderr, ">E Usage: %s\n",USAGE);
        GETHELP;
        exit(1);
    }
    if (!quiet)
    {
        fprintf(stderr, ">A pgtonauty");
        if (sswitch || gswitch)
            fprintf(stderr, " -");
        if (sswitch)
            fprintf(stderr, "s");
        if (gswitch)
            fprintf(stderr, "g");
        if (argnum > 0)
            fprintf(stderr, " %s",infilename);
        if (argnum > 1)
            fprintf(stderr, " %s",outfilename);
        fprintf(stderr, "\n");
    }
    if (gswitch)
        codetype = GRAPH6;
    else codetype = SPARSE6;
    if (infilename && infilename[0] == '-')
        infilename = NULL;
    infile = opengraphfile(infilename,&codetype,FALSE,1);
    if (!infile)
        exit(1);
    if (!infilename)
        infilename = "stdin";
    if (!outfilename || outfilename[0] == '-')
    {
        outfilename = "stdout";
        outfile = stdout;
    }
    else if ((outfile = fopen(outfilename,"w")) == NULL)
    {
        fprintf(stderr, "Can't open output file %s\n",outfilename);
        gt_abort(NULL);
    }
    
    if (!quiet)
        fprintf(stderr, ">Z Reading graphs from %s\n", infilename);
    while (fgets(l, BUFFER, infile) != NULL)
    {
        ++numread;
        for (i = 1; l[i] != '}'; )
        {
            n = atoi(l + i);
            while (l[i] != '{')
                ++i;
            while (l[i] != '}')
                ++i;
            ++i;
            while (l[i] == ',' || l[i] == ' ')
                ++i;
	    }
	    m = (++n + WORDSIZE - 1) / WORDSIZE;
	    for (i = 0; i < m * n; ++i)
            g[i] = 0;
        for (i = 1; l[i] != '}'; )
        {
			v1 = atoi(l + i);
			s = GRAPHROW(g, v1, m);
            while (l[i] != '{')
                ++i;
            ++i;
            while (1)
            {
                if (l[i] != '}')
                {
                    v2 = atoi(l + i);
                    ADDELEMENT(s, v2);
                }
                while (l[i] != ',' && l[i] != '}')
                    ++i;
                if (l[i++] == '}')
                    break;
                while (l[i] == ' ')
                    ++i;
            }
            while (l[i] == ',' || l[i] == ' ')
                ++i;
        }
        if (mswitch)
            writeadj(outfile, g, n);
        else if (pswitch)
            writepg(outfile, g, n);
        else if (zswitch)
            writetkz(outfile, g, n);
        else if (!uswitch)
            writeg6(outfile, g, 1, n);
        ++numwritten;
    }
    if (!quiet)
        fprintf(stderr, ">Z %lu graphs written to %s\n", numwritten, outfilename);

    return EXIT_SUCCESS;
}
