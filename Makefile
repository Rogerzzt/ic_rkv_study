export UVMF_HOME ?= ../../../sv_packs/tb/uvc_lib
export UVMF_VIP_LIBRARY_HOME ?=  ../../../sv_packs/tb/uvc_lib
export UVMF_PROJECT_DIR ?= ..
export VCS_LIC_EXPIRE_WARNING = 3

#############################
# User variables
#############################
NAME      = wrf1
TOP       = {hdl_top,hvl_top}
SEED     	= 1
COV      ?= 0
DOTCL    ?= 1
OUT      ?= out
VERB     ?= UVM_MEDIUM
TEST 		 ?= wrf1_smoke_test
DFILES  	= -F ../src/hdl/rtl.f
VFILES   += -top ../src/tb/hdl_top.sv \
						-top ../src/tb/hvl_top.sv
FFILES  	= -f ../src/tb/tb_uvm.f


#############################
# Environment variables
#############################
VCOMP_INC = +incdir+../../../sv_packs/tb/{common,uvc_lib,uvm}

VCOMP    = vlogan -full64 -ntb_opts uvm-1.2 -sverilog -timescale=1ns/10ps -nc ${VCOMP_INC} -kdb -l ${OUT}/log/comp.log
ELAB     = vcs -full64 -ntb_opts uvm-1.2 -Mlib=work -notice +nospecify +notimingcheck -kdb -debug_access+all -l ${OUT}/log/elab.log 
RUN      = ${OUT}/obj/${NAME}.simv -sv_lib /share/model_share/libdpi -l ${OUT}/log/vcs_run.log -sml +ntb_random_seed=${SEED} +UVM_TESTNAME=${TEST} -cm_dir ${CM_DIR} -cm_name ${CM_NAME} +UVM_VERBOSITY=${VERB}

COV_OPTS = -full64 -dir ${CM_DIR}
CM_DIR  ?= ${OUT}/${TEST}.vdb
CM_NAME ?= ${TEST}_${SEED}
SCRIPTS_DIR=../../../sv_packs/tb/common/scripts
##SIMRUNFILE 	= rkv_timer_sim_run.do

ifeq ($(WAVE),1)
RUN += -ucli -i ${SCRIPTS_DIR}/waves.do
endif
ifeq ($(COV),1)
	ELAB  += -cm line+cond+fsm+tgl+branch+assert -cm_dir ${CM_DIR}
	RUN   += -cm line+cond+fsm+tgl+branch+assert -covg_cont_on_error +COV_ENABLE=1
endif

prepare:
	mkdir -p ${OUT}/work
	mkdir -p ${OUT}/log
	mkdir -p ${OUT}/sim
	mkdir -p ${OUT}/obj

comp: prepare
	${VCOMP} 
	${VCOMP} ${DFILES} ${VFILES} ${FFILES}

elab: comp
	${ELAB} -top ${TOP} -o ${OUT}/obj/${NAME}.simv

runp:
	${RUN}

run: runp post_proc

verdi:
	Verdi -ssf wave.fsdb &

mergecov:
	urg -format both ${COV_OPTS}

verdicov:
	verdi -cov -covdir ${CM_DIR}

htmlcov:
	firefox urgReport/dashboard.html

clean:
	rm -rf ${OUT} 64 AN.DB DVEfiles csrc *.simv *.simv.daidir *.simv.vdb ucli.key
	rm -rf *.log* *.vpd *.h urgReport

post_proc:
	perl ${SCRIPTS_DIR}/sim_post_process.pl vcs_run.log
